from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer
from sklearn.feature_selection import VarianceThreshold, SelectKBest
from sklearn.pipeline import Pipeline
from sklearn_utils.preprocessing import *

from metabolitics.preprocessing import *
from metabolitics.utils import load_naming


def set_steps():
    pipe = dict()

    pipe['naming'] = FeatureRenaming(load_naming())

    vect = DictVectorizer(sparse=False)
    pipe['imputer'] = Pipeline([
        ('vect-imputer', vect),
        ('imputer-mean', Imputer(0, 'mean')),
        ('inv_vec-imputer', InverseDictVectorizer(vect)),
    ])

    vect = DictVectorizer(sparse=False)
    pipe['metabolic-standard-scaler'] = Pipeline([
        ('vect-standard', vect),
        ('metabolic-standard', StandardScalerByLabel('healthy')),
        ('inv_vec-standard', InverseDictVectorizer(vect)),
    ])

    pipe['fold-change-scaler'] = FoldChangeScaler('healthy')
    pipe['metabolitics-transformer'] = MetaboliticsTransformer()
    pipe['reaction-diff'] = ReactionDiffTransformer()

    vect1 = DictVectorizer(sparse=False)
    vect2 = DictVectorizer(sparse=False)
    vt = VarianceThreshold(0.1)
    skb = SelectKBest(k=100)
    pipe['feature-selection'] = Pipeline([
        ('vect-vt', vect1),
        ('vt', vt),
        ('inv_vec-vt', InverseDictVectorizer(vect1, vt)),
        ('vect-skb', vect2),
        ('skb', skb),
        ('inv_vec-skb', InverseDictVectorizer(vect2, skb)),
    ])

    pipe['pathway_transformer'] = PathwayTransformer()

    return pipe


class MetaboliticsPipeline(DynamicPipeline):
    steps = set_steps()

    default_steps = [
        'naming',
        'metabolic-standard-scaler',
        'metabolitics-transformer',
        'reaction-diff',
        'feature-selection',
        'pathway_transformer',
    ]
