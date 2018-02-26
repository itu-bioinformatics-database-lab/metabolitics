from sklearn.base import TransformerMixin

from sklearn_utils.utils import map_dict_list


class TransportPathwayElimination(TransformerMixin):

    black_list = ['Transport', 'Exchange', '_']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return map_dict_list(
            X, if_func=lambda k, v:
            all([not k.startswith(i) and k for i in self.black_list]))
