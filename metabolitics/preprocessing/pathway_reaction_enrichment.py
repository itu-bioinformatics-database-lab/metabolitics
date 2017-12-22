import cobra as cb
from functional import seq
from sklearn_utils.preprocessing import FunctionalEnrichmentAnalysis

import metabolitics.extensions
from metabolitics.utils import load_network_model


class PathwayReactionEnrichment(FunctionalEnrichmentAnalysis):
    """Functional Enrichment Analysis"""

    def __init__(self,
                 reference_label='healthy',
                 network_model='recon2',
                 **kwargs):
        '''
        :param str reference_label: label of refence values in the calculation
        :param str dataset_name: name of metabolitics network
        '''
        model = load_network_model(network_model)

        feature_groups = seq(model.reactions) \
                         .map(lambda r: (r.subsystem, '%s_dif' % r.id)) \
                         .filter(lambda x: not cb.Model.is_transport_subsystem(x[0])) \
                         .group_by_key() \
                         .to_dict()

        super().__init__(reference_label, feature_groups, **kwargs)
