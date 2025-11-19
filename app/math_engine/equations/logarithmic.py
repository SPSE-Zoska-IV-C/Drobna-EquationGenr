from root import Method

from math import sqrt, log10
from operator import sub, add, mul, truediv, pow
from fractions import Fraction
import sympy as sp
import random

### logarytmicke vety 
### substitucia 
### uprava na rovnaky zaklad
### podmienky

class Mixed_methods(Method):
    def create(self):
        if self.level == 'simple':
            self.create_simple()
        elif self.level == 'advanced':
            self.create_advanced()

    def create_simple(self):
        self.val_r = random.randint(2, 11)  # root of the logarithm
        self.val_log = random.randint(0, 6) # main logarithm of the equation
        self.val_x = self.val_r ** self.val_log

        self.roots = [self.val_x]
        self.equation = sp.Eq(sp.log(sp.symbols('x'), self.val_r), self.val_log)
        self.steps.append(self.equation)

    def create_advanced(self):
        pass


class Substitution(Method):
    def create(self):
        if self.level == 'simple':
            self.create_simple()
        elif self.level == 'advanced':
            self.create_advanced()

    def create_simple(self):
        pass

    def create_advanced(self):
        pass

