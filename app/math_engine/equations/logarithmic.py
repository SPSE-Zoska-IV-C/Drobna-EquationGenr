from root import Method, nmul, ndiv

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
        x = sp.symbols('x')

        left_side = self.val_a * (sp.log(x, sp.symbols(f'{self.val_r}')) ** 2) + self.val_b * sp.log(x, sp.symbols(f'{self.val_r}'))
        right_side = -self.val_c
        self.steps.append(sp.Eq(left_side, right_side))

        modifications = random.sample([add, sub, mul, nmul, truediv, ndiv], k=random.randint(1, 4))
        
        original_rs = right_side

        # Randomly modify both sides
        for func in modifications:
            n = random.randint(2, 5)
            if random.choice([True, False]):
                if isinstance(func(right_side, n), (int, float)):
                    if func(right_side, n) >= 10000 or func(right_side, n) == 0 or func(right_side, n) <= -10000 or int(func(right_side, n)*1000) != func(right_side, n)*1000:
                        n = sp.symbols(f'{n}')
                left_side = func(left_side, n)
                right_side = func(right_side, n)

        if right_side != original_rs:
            self.steps.append(sp.Eq(left_side, right_side))


        # Optionally wrap in parentheses or scale both sides
        if random.choice([True, False]):
            scale = random.choice([2, 3, 0.5, -1])
            left_side = scale * left_side
            right_side = scale * right_side
            self.steps.append(sp.Eq(left_side, right_side))

        self.equation = sp.Eq(left_side, right_side)


