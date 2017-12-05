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
            reaction.id: self._reaction_flux_diff(reaction, x)
            for reaction in self.model.reactions if '%s_max' % reaction.id in x
        } for x in X]

    def _reaction_flux_diff(self, reaction, x):
        f_score = lambda label: x[label] - self.healthy_flux[label]
        return sum(f_score('%s_%s' % (reaction.id, i)) for i in ['min', 'max'])
