from abc import ABC, abstractmethod

class Function(ABC):
    def __init__(self, coefficients=None):
        print(coefficients)
        self.coefficiens = coefficients if coefficients is not None else self.create_coefficiens()
        print('init ', self.coefficiens)
        self.parameters = self.get_parameters()

    @abstractmethod
    def create_coefficiens(self):
        '''Creates function coefficients, saved in self'''

    @abstractmethod
    def create_graph(self):
        '''Creates graph of function, saved in self'''

    @abstractmethod
    def get_parameters(self):
        '''Returns list of parameters of function, saved in self'''

