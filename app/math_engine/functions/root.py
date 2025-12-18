from abc import ABC, abstractmethod

class Function(ABC):
    def __init__(self, coefficients=None):
        self.coefficients = coefficients
        self.create_coefficients()
        self.get_parameters()

    @abstractmethod
    def create_coefficients(self):
        '''Creates function coefficients, saved in self'''

    @abstractmethod
    def create_graph(self):
        '''Creates graph of function, saved in self'''

    @abstractmethod
    def get_parameters(self):
        '''Returns list of parameters of function, saved in self'''

    @abstractmethod
    def get_inverse(self):
        '''Returns inverse of function, saved in self'''
        return Function