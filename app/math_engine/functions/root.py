from abc import ABC, abstractmethod

class Function(ABC):
    def __init__(self, coefficients=None):
        print(coefficients)
        self.coefficients = coefficients if coefficients is not None else self.create_coefficients()
        print('init ', self.coefficients)
        self.parameters = self.get_parameters()

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