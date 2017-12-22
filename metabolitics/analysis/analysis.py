import cobra

from sympy.core.singleton import S
from cobra.util import fix_objective_as_constraint
from cobra.flux_analysis import flux_variability_analysis

import metabolitics.extensions
from metabolitics.utils import load_network_model


class MetaboliticsAnalysis:
    '''
    Metabolitics analysis for metabolic dataset.
    '''

    def __init__(self, model, without_transports=True, timeout=10 * 60):
        '''
        :param model: cobra Model
        '''
        self.model = load_network_model(model)
        self.model.solver.configuration.timeout = timeout
        self.without_transports = without_transports

    def set_objective(self, measured_metabolites):
        '''
        Updates objective function for given measured metabolites.

        :param dict measured_metabolites: dict in which keys are metabolite names 
            and values are float numbers represent fold changes in metabolites. 
        '''
        self.clean_objective()
        for k, v in measured_metabolites.items():

            m = self.model.metabolites.get_by_id(k)
            total_stoichiometry = m.total_stoichiometry(
                self.without_transports)

            for r in m.producers(self.without_transports):
                update_rate = v * r.metabolites[m] / total_stoichiometry
                r.objective_coefficient += update_rate

    def add_constraint(self, measured_metabolites):
        '''
        Add measurements as constraint to model.

        :param dict measured_metabolites: dict in which keys are metabolite names 
            and values are float numbers represent fold changes in metabolites.
        '''
        self.set_objective(measured_metabolites)
        fix_objective_as_constraint(self.model)

    def variability_analysis(self, measured_metabolites):
        self.set_objective(measured_metabolites)
        return flux_variability_analysis(self.model)

    def clean_objective(self):
        '''
        Cleans previous objective.
        '''
        self.model.objective = S.Zero

    def copy(self):
        return self.__class__(self.model.copy(), self.without_transports)
