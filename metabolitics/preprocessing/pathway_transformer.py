from collections import defaultdict

from sklearn.base import TransformerMixin
from sklearn_utils.preprocessing import FeatureMerger

from metabolitics.utils import load_network_model


class PathwayTransformer(FeatureMerger):
    """Converts reaction level features to pathway level."""

    def __init__(self, network_model="recon2", metrics='mean'):
        model = load_network_model(network_model)
        features = defaultdict(list)

        for r in model.reactions:
            features[r.subsystem].append(r.id)

        super().__init__(features, metrics)
