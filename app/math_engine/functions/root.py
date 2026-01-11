from abc import ABC, abstractmethod

class Function(ABC):
    def __init__(self, coefficients=None):
        self.coefficients = coefficients
        if self.coefficients is None:
            self.create_coefficients()
        self.get_parameters()

    @abstractmethod
    def create_coefficients(self):
        '''Creates function coefficients, saved in self'''

    @abstractmethod
    def get_graph(self):
        '''Creates graph of function, saved in self'''

    @abstractmethod
    def get_parameters(self):
        '''Returns list of parameters of function'''

    @abstractmethod
    def get_inverse(self):
        '''Returns inverse of function'''

    @abstractmethod
    def get_latex_formula(self):
        '''Returns latex formula of function'''
    
    def get_coefficients(self):
        return self.coefficients
    
    def get_parameters(self):
        return self.parameters
    


    def get_graph(self):
        pass

    def get_type(self):
        return self.type

    