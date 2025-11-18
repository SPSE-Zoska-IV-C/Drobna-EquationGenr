import sympy as sp
from abc import ABC, abstractmethod



class Method(ABC):
    def __init__(self, level):
        self.level = level
        self.equation = None
        self.roots = []
        self.steps = []

        self.create() # self.equation, self.roots, self.steps

    @abstractmethod
    def create(self):
        '''manages creation of equation, its roots and solving steps based on level, saved in self'''
        
    @abstractmethod
    def create_simple(self):
        '''Creates simple equation and solving steps, saved in self'''
        
    @abstractmethod
    def create_advanced(self):
        '''Creates advanced equation and solving steps, saved in self'''
        
    def get_roots(self):
        return self.roots
    
    def get_equation(self):
        return self.equation
    


