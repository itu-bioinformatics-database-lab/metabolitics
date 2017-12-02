import unittest
import cobra as cb
from .analysis import MetaboliticsAnalysis


class TestMetaboliticsAnalysis(unittest.TestCase):
    def setUp(self):
        model = cb.test.create_test_model('salmonella')
        self.model = MetaboliticsAnalysis(model, without_transports=False)
        self.h2o2_p = model.metabolites.get_by_id('h2o2_p')

    def test_update_objective_coefficients(self):
        self.model.update_objective_coefficients({'h2o2_p': 1})
        for r in self.h2o2_p.producers():
            self.assertNotEqual(r.objective_coefficient, 0.0)
