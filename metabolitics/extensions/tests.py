import unittest

import cobra as cb
import cobra.test
from .metabolite_extantions import *
import math


class TestModelExtantion(unittest.TestCase):
    def test_is_transport_subsystem(self):
        self.assertTrue(
            cb.Model.is_transport_subsystem('Transport Outer Membrane'))
        self.assertTrue(
            cb.Model.is_transport_subsystem('Exchange Outer Membrane'))
        self.assertTrue(cb.Model.is_transport_subsystem(''))
        self.assertFalse(cb.Model.is_transport_subsystem('Outer Membrane'))


class TestMetaboliteExtantion(unittest.TestCase):
    def setUp(self):
        self.model = cb.test.create_test_model('salmonella')
        self.h2o_c = self.model.metabolites.get_by_id('h2o_c')
        self.pglyc_c = self.model.metabolites.get_by_id('2pglyc_c')
        self.hdd2coa_c = self.model.metabolites.get_by_id('hdd2coa_c')

    def test_is_border(self):
        self.assertEqual(self.h2o_c.is_border(), True)
        self.assertEqual(self.pglyc_c.is_border(), False)

    def test_producers(self):
        self.assertEqual(len(self.hdd2coa_c.producers()), 3)
        num_trans = len(self.h2o_c.producers()) - \
            len(self.h2o_c.producers(without_transports=True))
        self.assertEqual(num_trans, 6)

    def test_consumers(self):
        self.assertEqual(len(self.pglyc_c.consumers()), 1)

    def test_total_stoichiometry(self):
        self.assertEqual(self.hdd2coa_c.total_stoichiometry(), 3)
