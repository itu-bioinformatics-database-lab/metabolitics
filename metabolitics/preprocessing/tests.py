import unittest

from .metabolitics_transformer import MetaboliticsTransformer


class TestMetaboliticsTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = MetaboliticsTransformer('textbook')
        self.X = [{'accoa_c': 1}]

    def test__transform(self):
        results = self.transformer._transform(self.X[0])
        self.assertIn('GLUDy_max', results)
        self.assertIn('GLUDy_min', results)

    def test_fit_transform(self):
        results = self.transformer.fit_transform(self.X)
        self.assertIn('GLUDy_max', results[0])
        self.assertIn('GLUDy_min', results[0])
