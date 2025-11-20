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
        self.val_r = random.randint(2, 11)  # root of the logarithm
        self.val_log1 = random.randint(0, 6) # main logarithm of the equation
        self.val_log2 = random.randint(0, 6) # main logarithm of the equation
        self.val_x1 = self.val_r ** self.val_log1 # 
        self.val_x2 = self.val_r ** self.val_log2 # 


        self.val_q = -self.val_log1 # coefficient of the equation
        self.val_p = -self.val_log2 # constant of the equation

        self.val_a = random.choice([i for i in range(-10, 11) if i != 0]) # coefficient of the equation
        self.val_b = self.val_a * (self.val_p + self.val_q)
        self.val_c = self.val_a * (self.val_p * self.val_q)

        # variables
        t = sp.symbols('t')
        
        # quadratic equation
        quad_eq = sp.Eq(self.val_a * (t ** 2) + self.val_b * t + self.val_c, 0)

        self.steps.append(quad_eq)
        self.steps.append(sp.Eq(sp.Symbol('t'), sp.log(sp.symbols('x'), sp.symbols(f'{self.val_r}'))))

        self.roots = [self.val_x1, self.val_x2]

        if self.level == 'simple':
            self.create_simple()
        elif self.level == 'advanced':
            self.create_advanced()

    def create_simple(self):
        self.equation = sp.Eq(self.val_a * (sp.log(sp.symbols('x'), sp.symbols(f'{self.val_r}')) ** 2) + self.val_b * sp.log(sp.symbols('x'), sp.symbols(f'{self.val_r}')) , - self.val_c)
        self.steps.append(self.equation)

    def create_advanced(self):
        pass

