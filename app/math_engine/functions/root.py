from abc import ABC, abstractmethod

class Function(ABC):
    @abstractmethod
    def __init__(self, coefficients=None):
        self.coefficiens = coefficients if not None else self.create_coefficiens()

    @abstractmethod
    def create_coefficiens(self):
        '''Creates function coefficients, saved in self'''

    @abstractmethod
    def create_graph(self):
        '''Creates graph of function, saved in self'''

    def get_parameters(self):
        '''Returns list of parameters of function, saved in self'''

# obor hodnot
# definicny obor
# priesecniky
# parametre
# graf - responzivny, vypocet parametrov ovplyvnujucich graf
# inverzna funkcia - instancia funkcie