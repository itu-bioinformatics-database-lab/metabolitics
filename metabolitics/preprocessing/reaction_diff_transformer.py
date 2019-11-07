from sklearn.base import TransformerMixin
from sklearn_utils.utils import average_by_label

from metabolitics.utils import load_network_model


class ReactionDiffTransformer(TransformerMixin):
    """Scaler reaction by diff"""

    def __init__(self, network_model="recon2", reference_label='healthy'):
        self.model = load_network_model(network_model)
        self.reference_label = reference_label

    def fit(self, X, y):
        self.healthy_flux = average_by_label(X, y, self.reference_label)
        return self

    def transform(self, X, y=None):
        return [{
            reaction.id: self._reaction_flux_diff(reaction.id, x)
            for reaction in self.model.reactions
            if self._is_valid_for_diff(reaction.id, x)
        } for x in X]

    def _reaction_flux_diff(self, r_id: str, x):
        r_max, r_min = self._r_max_min(r_id)
        h_max = self.healthy_flux[r_max]
        h_min = self.healthy_flux[r_min]
        r_max, r_min = x[r_max], x[r_min]
        
        r_rev_max = abs(min(r_min, 0))
        r_rev_min = abs(min(r_max, 0))
        r_max = max(r_max, 0)
        r_min = max(r_min, 0)

        h_rev_max = abs(min(h_min, 0))
        h_rev_min = abs(min(h_max, 0))
        h_max = max(h_max, 0)
        h_min = max(h_min, 0)
        
        for_score = (r_max - h_max) + (r_min - h_min)
        rev_score = (r_rev_max - h_rev_max) + (r_rev_min - h_rev_min)
        
        return for_score + rev_score
        
    def _r_max_min(self, r_id):
        return '%s_max' % r_id, '%s_min' % r_id

    def _is_valid_for_diff(self, r_id, x):
        return all(i in x and i in self.healthy_flux
                   for i in self._r_max_min(r_id))
