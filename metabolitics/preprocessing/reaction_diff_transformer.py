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
        return sum(map(lambda r: x[r] - self.healthy_flux[r],
                       self._r_max_min(r_id)))

    def _r_max_min(self, r_id):
        return '%s_max' % r_id, '%s_min' % r_id

    def _is_valid_for_diff(self, r_id, x):
        return all(i in x and i in self.healthy_flux
                   for i in self._r_max_min(r_id))
