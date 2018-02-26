import unittest

import cobra as cb

from .io_utils import load_network_model, load_metabolite_mapping


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

    def test_load_naming(self):
        for i in {'kegg', 'pubChem', 'cheBl', 'hmdb', 'toy'}:
            self.assertGreater(len(load_metabolite_mapping(i)), 0)
