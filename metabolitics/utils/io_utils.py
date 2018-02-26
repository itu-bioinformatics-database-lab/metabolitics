import json
import os

import cobra as cb
import cobra.test

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATASET_PATH = os.path.join(PROJECT_ROOT, 'datasets')


def load_network_model(model):
    '''
    Loads metabolic network models in metabolitics.

    :param str model: model name
    '''
    if type(model) == str:
        if model in ['ecoli', 'textbook', 'salmonella']:
            return cb.test.create_test_model(model)
        elif model == 'recon2':
            return cb.io.load_json_model('%s/network_models/%s.json' %
                                         (DATASET_PATH, model))
    if type(model) == cb.Model:
        return model


def load_metabolite_mapping(naming_file='pubChem'):
    '''
    Loads metabolite name mapping from different databases to recon.

    :param str naming_file: names of databases
    valid options {'kegg', 'pubChem', 'cheBl', 'hmdb', 'toy'}
    '''

    with open('%s/naming/%s-mapping.json' % (DATASET_PATH, naming_file)) as f:
        return json.load(f)
