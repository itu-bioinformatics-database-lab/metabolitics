import unittest
import cobra as cb
from .analysis import MetaboliticsAnalysis


class TestMetaboliticsAnalysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = MetaboliticsAnalysis(
            'textbook', without_transports=False)
        self.accoa_c = self.analyzer.model.metabolites.get_by_id('accoa_c')
        self.measurements = {'accoa_c': 1}

    def test_set_objective(self):
        self.analyzer.set_objective(self.measurements)
        for r in self.accoa_c.producers():
            self.assertNotEqual(r.objective_coefficient, 0.0)

    def test_add_constraint(self):
        self.analyzer.add_constraint(self.measurements)

    def test_variability_analysis(self):
        df = self.analyzer.variability_analysis(self.measurements)
        self.assertIsNotNone(df)

    def test_copy(self):
        self.assertIsNotNone(self.analyzer.copy())
