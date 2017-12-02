import unittest

import cobra as cb

from .io_utils import load_network_model


class TestIOUtils(unittest.TestCase):
    def test_load_network_model(self):
        model = cb.Model()
        loaded_model = load_network_model(model)
        self.assertEqual(model, loaded_model)

        textbook = load_network_model('textbook')
        self.assertEqual(textbook.id, 'e_coli_core')

        recon2 = load_network_model('recon2')
        self.assertGreater(len(recon2.reactions), 1000)
        self.assertGreater(len(recon2.metabolites), 1000)
