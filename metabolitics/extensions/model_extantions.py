import cobra as cb

black_list = {'Transport', 'Exchange'}


def subsystems(self):
    ''' Gives subsystems of reactions '''
    return set([r.subsystem for r in self.reactions])


@staticmethod
def is_transport_subsystem(subsystem):
    '''Check that subsystem is exchange or transport subsystem'''
    return (not subsystem) or any(subsystem.startswith(i) for i in black_list)


cb.Model.subsystems = subsystems
cb.Model.is_transport_subsystem = is_transport_subsystem
