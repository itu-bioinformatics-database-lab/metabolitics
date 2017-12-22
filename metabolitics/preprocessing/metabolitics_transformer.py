from joblib import Parallel, delayed
from sklearn.base import TransformerMixin

from metabolitics.analysis import MetaboliticsAnalysis


class MetaboliticsTransformer(TransformerMixin):
    """Performs metabolitics analysis and 
    convert metabolitic value into reaction min-max values."""

    def __init__(self, network_model="recon2", n_jobs=-1):
        '''
        :param network_model: cobra.Model or name of the model. 
        :param n_jobs: the maximum number of concurrently running jobs.
        '''
        self.analyzer = MetaboliticsAnalysis(network_model)
        self.n_jobs = n_jobs

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        '''
        :param X: list of dict which contains metabolic measurements.
        '''
        return Parallel(n_jobs=self.n_jobs)(delayed(self._transform)(x)
                                            for x in X)

    def _transform(self, x):
        x_t = dict()
        analyzer = self.analyzer.copy()

        for r in analyzer.variability_analysis(x).itertuples():
            x_t['%s_max' % r.Index] = r.maximum
            x_t['%s_min' % r.Index] = r.minimum

        return x_t
