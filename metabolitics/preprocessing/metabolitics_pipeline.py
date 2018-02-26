from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.feature_selection import VarianceThreshold, SelectKBest
from sklearn.pipeline import Pipeline
from sklearn_utils.preprocessing import *

from metabolitics.preprocessing import *
from metabolitics.utils import load_metabolite_mapping


class MetaboliticsPipeline(DynamicPipeline):

    default_steps = [
        'metabolite-name-mapping',
        'standard-scaler',
        'metabolitics-transformer',
        'reaction-diff',
        'feature-selection',
        'pathway-transformer',
    ]

    @classmethod
    def make_pipeline(cls, selected_steps):
        steps = list()

        if 'metabolite-name-matching' in selected_steps:
            steps.append(
                ('naming', FeatureRenaming(load_metabolite_mapping())))

        for i in {'kegg', 'pubChem', 'cheBl', 'hmdb', 'toy'}:
            if 'metabolite-name-matching-%s' % i in selected_steps:
                steps.append(
                    ('naming-%s' % i, FeatureRenaming(load_metabolite_mapping(i))))

        if 'imputer' in selected_steps:
            vect = DictVectorizer(sparse=False)
            steps.extend([
                ('vect-imputer', vect),
                ('imputer-mean', Imputer(0, 'mean')),
                ('inv_vec-imputer', InverseDictVectorizer(vect)),
            ])

        if 'standard-scaler' in selected_steps:
            vect = DictVectorizer(sparse=False)
            steps.extend([
                ('vect-standard', vect),
                ('standard', StandardScaler()),
                ('inv_vec-standard', InverseDictVectorizer(vect)),
            ])

        if 'metabolic-standard-scaler' in selected_steps:
            vect = DictVectorizer(sparse=False)
            steps.extend([
                ('vect-metabolic-standard', vect),
                ('metabolic-standard', StandardScalerByLabel('healthy')),
                ('inv_vec-metabolic-standard', InverseDictVectorizer(vect)),
            ])

        if 'fold-change-scaler' in selected_steps:
            steps.append(('fold-change-scaler', FoldChangeScaler('healthy')))

        if 'metabolitics-transformer' in selected_steps:
            steps.append(('metabolitics-transformer',
                          MetaboliticsTransformer()))

        if 'reaction-diff' in selected_steps:
            steps.append(('reaction-diff', ReactionDiffTransformer()))

        if 'feature-selection' in selected_steps:
            vect1 = DictVectorizer(sparse=False)
            vect2 = DictVectorizer(sparse=False)
            vt = VarianceThreshold(0.1)
            skb = SelectKBest(k=100)
            steps.extend([
                ('vect-vt', vect1),
                ('vt', vt),
                ('inv_vec-vt', InverseDictVectorizer(vect1, vt)),
                ('vect-skb', vect2),
                ('skb', skb),
                ('inv_vec-skb', InverseDictVectorizer(vect2, skb)),
            ])

        if 'pathway-transformer' in selected_steps:
            steps.append(('pathway-transformer', PathwayTransformer()))

        if 'transport-pathway-elimination' in selected_steps:
            steps.append(
                ('transport-pathway-elimination', TransportPathwayElimination()))

        return Pipeline(steps)
