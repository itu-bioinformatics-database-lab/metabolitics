import unittest

from .metabolitics_transformer import MetaboliticsTransformer
from .pathway_reaction_enrichment import PathwayReactionEnrichment
from .reaction_diff_transformer import ReactionDiffTransformer
from .pathway_transformer import PathwayTransformer
from .metabolitics_pipeline import MetaboliticsPipeline
from .transport_pathway_elimination import TransportPathwayElimination


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


class TestReactionDiffTransformer(unittest.TestCase):
    def setUp(self):
        self.scaler = ReactionDiffTransformer()
        self.h = {'TAXOLte_max': 1, 'TAXOLte_min': -1}
        self.X = [self.h, {'TAXOLte_max': 2,
                           'TAXOLte_min': 1, 'MAL_Lte_max': 1}]
        self.y = ['healthy', 'bc']

    def test_fit(self):
        self.scaler.fit(self.X, self.y)
        self.assertEqual(self.scaler.healthy_flux, self.h)

    def test_fit_transform(self):
        sub_scores = self.scaler.fit_transform(self.X, self.y)
        self.assertEqual(sub_scores, [{'TAXOLte': 0}, {'TAXOLte': 3}])


class TestPathwayTransformer(unittest.TestCase):
    def setUp(self):
        self.model = PathwayTransformer()
        self.X = [{'TAXOLte': 1, 'MAL_Lte': -4}]

    def test_fit_transform(self):
        X_t = self.model.fit_transform(self.X)
        self.assertTrue(X_t, [{'Transport, extracellular': -1.5}])


class TestPathwayReactionEnrichment(unittest.TestCase):
    def setUp(self):
        self.X = [{
            'GLUDym_dif': 1,
            'GLUNm_dif': -1,
            'GLNS_dif': 0.0001,
            'P5CDm_dif': 100
        }, {
            'GLUDym_dif': 1,
            'GLUNm_dif': 2,
            'GLNS_dif': -1
        }]
        self.y = ['healthy', 'x']

        self.preprocessing = PathwayReactionEnrichment()

    def test_init(self):
        glu = self.preprocessing.feature_groups['Glutamate metabolism']

        self.assertTrue('GLUDym_dif' in glu)
        self.assertTrue('GLUNm_dif' in glu)
        self.assertTrue('GLNS_dif' in glu)
        self.assertTrue('P5CDm_dif' in glu)

    def test_fit(self):
        self.preprocessing.fit(self.X, self.y)
        self.assertEqual(dict(self.preprocessing._references), self.X[0])

    def test_transform(self):
        pvals = self.preprocessing.fit_transform(self.X, self.y)
        self.assertEqual(list(pvals[0].keys())[0], 'Glutamate metabolism')
        self.assertEqual(list(pvals[0].values())[0], 1)


class TestMetaboliticsPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = MetaboliticsPipeline()

    def test_pipeline(self):
        self.assertGreater(len(self.pipeline.steps), 0)


class TestTransportElimination(unittest.TestCase):
    def setUp(self):
        self.data = [
            {'Transport, a': 0, 'b': 2, '': 1},
            {'a': 0, 'Transport, b': 1}
        ]
        self.tranformer = TransportPathwayElimination()

    def test_transform(self):
        expected = [{'b': 2}, {'a': 0}]
        calculated = self.tranformer.transform(self.data)
        self.assertEqual(calculated, expected)
