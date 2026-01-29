from math_engine.equations.root import Method, ndiv, nmul

from math import sqrt, log10
from operator import sub, add, mul, truediv, pow
from fractions import Fraction
import sympy as sp
import random


class Substitution(Method):
    def create(self):
        self.val_r = random.randint(2, 6)  # root of the exponent x

        self.val_x1 = random.randint(0, 10 - self.val_r) # main x of the equation
        self.val_x2 = random.randint(0, 10 - self.val_r) # main x of the equation

        self.val_t1 = self.val_r ** self.val_x1 # main power 1 of the equation
        self.val_t2 = self.val_r ** self.val_x2 # main power 2 of the equation
        self.val_q = -self.val_t1 # coefficient of the equation
        self.val_p = -self.val_t2 # constant of the equation

        self.val_a = random.choice([i for i in range(-10, 11) if i != 0]) # coefficient of the equation
        self.val_b = self.val_a * (self.val_p + self.val_q)
        self.val_c = self.val_a * (self.val_p * self.val_q)

        self.steps.append(rf"K = \{{{self.val_x1},\, {self.val_x2}\}}")
        self.steps.append('\n')

        # variables
        t = sp.symbols('t')
        
        # quadratic equation
        quad_eq = sp.Eq(self.val_a * (t ** 2) + self.val_b * t + self.val_c, 0)
        
        self.steps.append(r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
        self.steps.append('\n')
        self.steps.append(rf"c = {self.val_c}")
        self.steps.append('\n')
        self.steps.append(rf"b = {self.val_b}")
        self.steps.append('\n')
        self.steps.append(rf"a = {self.val_a}")
        self.steps.append('\n')
        self.steps.append(sp.latex(quad_eq))
        self.steps.append('\n')
        self.steps.append(sp.latex(sp.Eq(sp.symbols('t'), self.val_r**sp.symbols("x"))))
        self.steps.append('\n')

        self.roots = [self.val_x1, self.val_x2]

        # main equation
        if self.level == 'simple':
            self.create_simple()
            self.steps.reverse()
        elif self.level == 'advanced':
            self.create_advanced()
            self.steps.reverse()
    
    def create_function_coefficients(self):
        self.func_coefs = None

    def create_simple(self):
        self.equation = sp.Eq(self.val_a * (self.val_r ** (2*sp.symbols('x'))) + self.val_b * (self.val_r ** sp.symbols('x')), -self.val_c)
        self.steps.append(sp.latex(self.equation))
        self.steps.append('\n')
  
    def create_advanced(self):
        x = sp.symbols('x')

        left_side = self.val_a * (self.val_r ** (2 * x)) + self.val_b * (self.val_r ** x)
        right_side = -self.val_c
        self.steps.append(sp.latex(sp.Eq(left_side, right_side)))
        self.steps.append('\n')

        modifications = random.sample([add, sub, mul, nmul, truediv, ndiv], k=random.randint(1, 3))
        
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
                self.steps.append(sp.latex(sp.Eq(left_side, right_side)))
                self.steps.append('\n')


        # Optionally wrap in parentheses or scale both sides
        if random.choice([True, False]):
            scale = random.choice([2, 3, 0.5, -1])
            left_side = scale * left_side
            right_side = scale * right_side
            self.steps.append(sp.latex(sp.Eq(left_side, right_side)))
            self.steps.append('\n')

        self.equation = sp.Eq(left_side, right_side)

    def get_equation(self):
        return sp.latex(self.equation)
    


class Matching_bases(Method):
    def create(self):
        self.val_r = random.randint(2, 10)  # root of the exponent x
        self.val_x = random.randint(-3, 5) # main x of the equation

        self.roots = [self.val_x]
        self.steps.append(sp.latex(f'K = {self.val_x}'))
        self.steps.append('\n')

        if self.level == 'simple':
            self.create_simple()
            self.steps.reverse()
        elif self.level == 'advanced':
            self.create_advanced()
            self.steps.reverse()
    
    def create_function_coefficients(self): # a*b**x + k
        self.func_coefs.update({'val_a': 1, 
                                'val_bn': self.val_r,
                                'val_bd': 1,
                                'val_v': 0,
                                'val_n': 1,
                                'val_k': sp.Rational(-(self.val_r**(self.val_x))).limit_denominator(1000), 
                                'val_px': self.val_x, 
                                'val_py': sp.Rational(1 - (self.val_r**(self.val_x))).limit_denominator(1000)})

    def create_simple(self):
        if self.val_x < 0:
            self.val_t = sp.symbols(f'1/{self.val_r ** abs(self.val_x)}')
        else:
            self.val_t = self.val_r ** self.val_x # main power of the equation

        x = sp.symbols('x')
        self.equation = sp.Eq(self.val_r ** x, self.val_t)
        self.steps.append(sp.latex(self.equation))
        self.steps.append('\n')
    
    def create_advanced(self):
        modifs_exp_signs = random.choices([add, sub, mul, nmul, truediv, ndiv], k=random.randint(1, 2))
        modifs_base_signs = random.choices([add, sub, mul, nmul, truediv, ndiv], k=random.randint(1, 2))

        right_exp = self.val_x
        symb_x = sp.symbols('x')

        for function in modifs_exp_signs:
            n = random.randint(1,3) if random.choice([True, False]) or self.val_x == 0 else self.val_x 
            if isinstance(function(right_exp, n), (int, float)):
                if n == self.val_x and (function != mul and function != nmul):
                    symb_x = function(symb_x, sp.symbols('x'))
                    right_exp = function(right_exp, sp.symbols('x'))
                    continue 
                if int(function(right_exp, n)*1000) != function(right_exp, n)*1000 or function(right_exp, n) > 10000 or function(right_exp, n) == 0:
                    n = sp.symbols(f'{n}')
                
            symb_x = function(symb_x, n)
            right_exp = function(right_exp, n)
     
        if isinstance(right_exp, int) or isinstance(right_exp, float) and int((self.val_r ** right_exp)*1000) != (self.val_r ** right_exp)*1000:
            right_exp = sp.symbols(f'{right_exp}')
        
        right_side = self.val_r ** right_exp
        left_side = self.val_r ** symb_x
        if symb_x != sp.symbols('x'):
            self.steps.append(sp.latex(sp.Eq(left_side, right_side)))
            self.steps.append('\n')
        
        old_r, old_l = right_side, left_side

        for function in modifs_base_signs:
            n = random.choice([1,2,4,5]) if random.choice([True, False]) else self.val_r ** self.val_x
            if n == self.val_r ** self.val_x:
                right_side = function(right_side, self.val_r ** sp.symbols('x'))
                left_side = function(left_side, self.val_r ** sp.symbols('x'))
                continue

            right_side = function(right_side, n)
            left_side = function(left_side, n)
        
        if right_side != old_r or left_side != old_l:
            self.steps.append(sp.latex(sp.Eq(left_side, right_side)))
            self.steps.append('\n')
        self.equation = sp.Eq(left_side, right_side)

    def get_equation(self):
        return sp.latex(self.equation)

class Logarithm(Method):
    def create(self):
        self.func_n_right = self.number_right = random.randint(10, 100)
        self.func_n_left = self.number_left = random.randint(10, 100)
        self.val_x = log10(self.number_right)/log10(self.number_left)

        self.roots = [self.val_x]
        self.steps.append(f'K = \\frac{{\\log({self.number_right})}}{{\\log({self.number_left})}}')
        self.steps.append('\n')

        if self.level == 'simple':
            self.create_simple()
            self.steps.reverse()
        elif self.level == 'advanced':
            self.create_advanced()
            self.steps.reverse()

    def create_function_coefficients(self):# a*b**x + k
        self.func_coefs.update({'val_a': 1, 
                                'val_n': 1,
                                'val_v': 0,
                                'val_k': -self.func_n_right, 
                                'val_px': sp.log(sp.symbols(f'{self.func_n_right}'), self.func_n_left), 
                                'val_py': 1 - self.func_n_right, 
                                'val_bn': self.func_n_left,
                                'val_bd': 1})
    
    def create_simple(self):
        x = sp.symbols('x')
        self.equation = sp.Eq(self.number_left ** x, self.number_right)
        self.steps.append(sp.latex(self.equation))
        self.steps.append('\n')

    def create_advanced(self):
        x = sp.symbols('x')
        self.equation = sp.Eq(self.number_left ** x, self.number_right)
        self.steps.append(sp.latex(self.equation))
        self.steps.append('\n')

        modifs_exp_signs = random.choices([add, sub, mul], k=random.randint(1, 2))
        modifs_base_signs = random.choices([add, sub, mul, nmul, truediv, ndiv], k=random.randint(1, 2))
        
        symb_x = sp.symbols('x')

        for function in modifs_exp_signs:
            n = random.randint(1,3)
            if function == add:
                if isinstance(self.number_right, (int, float)) and (int((self.number_right * (self.number_left ** n))*1000) != (self.number_right * (self.number_left ** n))*1000 or self.number_right * (self.number_left ** n) > 10000 or self.number_right * (self.number_left ** n) == 0 or self.number_right * (self.number_left ** n) < -10000):
                    n = sp.symbols(f'{n}')
                self.number_right = self.number_right * (self.number_left ** n)
            elif function == sub:
                if isinstance(self.number_right, (int, float)) and (int((self.number_right / (self.number_left ** n))*1000) != (self.number_right / (self.number_left ** n))*1000 or self.number_right / (self.number_left ** n) > 10000 or self.number_right / (self.number_left ** n) == 0 or self.number_right / (self.number_left ** n) < -10000):
                    n = sp.symbols(f'{n}')
                self.number_right = self.number_right / (self.number_left ** n)
            elif function == mul:
                if isinstance(self.number_right, (int, float)) and (int((self.number_right ** n)*1000) != (self.number_right ** n)*1000 or self.number_right ** n > 10000 or self.number_right ** n == 0 or self.number_right ** n < -10000):
                    n = sp.symbols(f'{n}')
                self.number_right = self.number_right ** n

            symb_x = function(symb_x, n)
        self.number_left = self.number_left ** symb_x

        step = sp.Eq(self.number_left, self.number_right, evaluate=False)
        self.steps.append(sp.latex(step))
        self.steps.append('\n')

        for function in modifs_base_signs:
            n = random.choice([1,2,4,5])
            self.number_right = function(self.number_right, n)
            self.number_left = function(self.number_left, n)
        
        self.steps.append(sp.latex(sp.Eq(self.number_left, self.number_right)))
        self.steps.append('\n')
        self.equation = sp.Eq(self.number_left, self.number_right)

    def get_equation(self):
        return sp.latex(self.equation)

