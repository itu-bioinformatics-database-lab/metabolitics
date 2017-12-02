'''Extantion Methods for Metabolites'''

import math
import json

import cobra as cb
from .model_extantions import *


def connected_subsystems(self):
    '''Connected Subsystem of metabolite'''
    return set([r.subsystem for r in self.reactions])


def is_border(self):
    ''' Extantion method to check metabolite in model is border'''
    return len(self.connected_subsystems()) > 1


def producers(self, without_transports=False):
    reactions = filter(lambda r: r.metabolites[self] > 0, self.reactions)
    if without_transports:
        reactions = filter(
            lambda r: not cb.Model.is_transport_subsystem(r.subsystem),
            reactions)
    return list(reactions)


def consumers(self):
    return [r for r in self.reactions if r.metabolites[self] < 0]


def total_stoichiometry(self, without_transports=False):
    return sum(r.metabolites[self] for r in self.producers(without_transports))


cb.Metabolite.connected_subsystems = connected_subsystems
cb.Metabolite.is_border = is_border
cb.Metabolite.producers = producers
cb.Metabolite.consumers = consumers
cb.Metabolite.total_stoichiometry = total_stoichiometry
