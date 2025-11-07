import random
import sympy as sp
from abc import ABC, abstractmethod
from math import sqrt, log10
from operator import sub, add, mul, truediv, pow
from fractions import Fraction

class Method(ABC):
    def __init__(self, level):
        self.level = level
        self.equation, self.roots = self.create()
        self.steps = self.solving_steps()

    @abstractmethod
    def create(self):
        '''Creates simple equation and its roots'''
        return sp.Eq(), list()

    @abstractmethod
    def solving_steps(self):
        '''list of steps to solve equation'''
        return list()
    
    @abstractmethod
    def create_advanced(self):
        '''Creates advanced equation and its roots'''
        return sp.Eq(), list()
    
    def get_roots(self):
        return self.roots
    
    def get_equation(self):
        return self.equation
    


def nmul(a, b):
    try:
        return -(a * b)
    except:
        return -(sp.symbols(f'{a}') * sp.symbols(f'{b}'))


def ndiv(a, b):
    try:
        return -(a / b)
    except:
        return -(sp.symbols(f'{a}') / sp.symbols(f'{b}'))


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

        # variables
        t = sp.symbols('t')
        x = sp.symbols('x')
        
        # quadratic equation
        quad_eq = sp.Eq(self.val_a * (t ** 2) + self.val_b * t + self.val_c, 0)
        # print('kvad eq:', quad_eq)

        # main equation
        if self.level == 'easy':
            eq = sp.Eq(self.val_a * (self.val_r ** (2*x)) + self.val_b * (self.val_r ** x), -self.val_c)
        else:
            self.exponents = [self.val_a, self.val_b, self.val_c, self.val_r]
            self.roots = [self.val_x1, self.val_x2]
            eq = self.create_advanced()

        return eq, [self.val_x1, self.val_x2]
    
    def create_advanced(self):
        x = sp.symbols('x')
        a, b, c, r = self.exponents

        left_side = a * (r ** (2 * x)) + b * (r ** x)
        right_side = -c

        modifications = random.sample(
            [add, sub, mul, nmul, truediv, ndiv], 
            k=random.randint(1, 3)
        )

        # Modify exponents slightly (like x → x+1 or x-2)
        shift1 = random.randint(-2, 2)
        self.val_x1, self.val_x2 = self.val_x1 - shift1, self.val_x2 - shift1
        left_side = a * (r ** (2 * (x + shift1))) + b * (r ** (x + shift1))
        right_side = (a * (r ** (2 * (self.val_x1 + shift1))) + b * (r ** (self.val_x1 + shift1)))
        
        # Randomly modify both sides
        for func in modifications:
            n = random.randint(1, 5)
            if random.choice([True, False]):
                left_side = func(left_side, n)
                right_side = func(right_side, n)


        # Optionally wrap in parentheses or scale both sides
        if random.choice([True, False]):
            scale = random.choice([2, 3, 0.5, -1])
            left_side = scale * left_side
            right_side = scale * right_side

        eq = sp.Eq(left_side, right_side)
        return eq


        
    def solving_steps(self):
        return []


class Matching_bases(Method):
    def create(self):
        self.val_r = random.randint(2, 11)  # root of the exponent x
        self.val_x = random.randint(-3, 5) # main x of the equation

    
        if self.val_x < 0:
            self.val_t = sp.symbols(f'1/{self.val_r ** abs(self.val_x)}')
        else:
            self.val_t = self.val_r ** self.val_x # main power of the equation

        x = sp.symbols('x')
        if self.level == 'easy':
            eq = sp.Eq(self.val_r ** x, self.val_t)
        else:
            self.exponents = [self.val_r, x] # not adding right side, since it is just the result of the left side
            self.roots = [self.val_x]
            eq, self.val_x = self.create_advanced() # [Number, sign, number, exponent]

        return eq, [self.val_x]
    


    def solving_steps(self):
        return []
    
    def create_advanced(self):
        modifs_exp_signs = random.choices([add, sub, mul, nmul, truediv, ndiv], k=random.randint(1, 3))
        modifs_base_signs = random.choices([add, sub, mul, nmul, truediv, ndiv], k=random.randint(1, 4))

        right_exp = self.val_x
        symb_x = sp.symbols('x') 


        for function in modifs_exp_signs:
            n = random.randint(1,3) if random.choice([True, False]) or self.val_x == 0 else self.val_x 
            if isinstance(function(right_exp, n), int) or isinstance(function(right_exp, n), float):
                if n == self.val_x:
                    symb_x = function(symb_x, sp.symbols('x'))
                    right_exp = function(right_exp, sp.symbols('x'))
                    continue 
                if int(function(right_exp, n)*1000) != function(right_exp, n)*1000 or function(right_exp, n) > 10000:
                    n = sp.symbols(f'{n}')
            symb_x = function(symb_x, n)
            right_exp = function(right_exp, n)


        if isinstance(right_exp, int) or isinstance(right_exp, float) and int((self.val_r ** right_exp)*1000) != (self.val_r ** right_exp)*1000:
                right_exp = sp.symbols(f'{right_exp}')
                

        right_side = self.val_r ** right_exp
        left_side = self.val_r ** symb_x


        for function in modifs_base_signs:
            n = random.choice([1,2,4,5]) if random.choice([True, False]) else self.val_r ** self.val_x
            if n == self.val_r ** self.val_x:
                right_side = function(right_side, self.val_r ** sp.symbols('x'))
                left_side = function(left_side, self.val_r ** sp.symbols('x'))
                continue

            right_side = function(right_side, n)
            left_side = function(left_side, n)
        
        eq = sp.Eq(left_side, right_side)
        return eq, self.val_x

class Logarithm(Method): # prerobit
    def create(self):
        number_right = random.randint(10, 100)
        number_left = random.randint(10, 100)
        val_x = log10(number_right)/log10(number_left)

        x = sp.symbols('x')
        self.val_x = val_x
        if self.level == 'easy':
            eq = sp.Eq(number_left ** x, number_right)
            print('root:', log10(number_right)/log10(number_left))

        else:
            self.exponents = [number_left, x, number_right] # need number right, since val_x is most likely irrational
            self.roots = [self.val_x]
            eq = self.create_advanced()

        return eq, [self.val_x]
    
    def create_advanced(self):
        x = sp.symbols('x')
        base, _, rhs_val = self.exponents  # base = number_left, rhs_val = number_right

        # --- helper functions ---
        def clean_num(n):
            """Return a neat, small numeric constant (no long floats or huge ints)."""
            if n == 0:
                return 0

            # Convert float → rational
            if isinstance(n, float):
                f = Fraction(n).limit_denominator(10)
                if f.denominator == 1:
                    n = f.numerator
                else:
                    n = sp.Rational(f.numerator, f.denominator)

            # Cap large integers
            if isinstance(n, int) and abs(n) > 99999:
                n = sp.Rational(n, random.randint(50, 200))  # scale down
            elif isinstance(n, int) and abs(n) > 20:
                # represent as product for variety
                k = random.randint(2, 5)
                if n % k == 0:
                    n = sp.Mul(k, n // k, evaluate=False)

            # Cap any remaining large rationals
            if isinstance(n, sp.Rational):
                if abs(n.p) > 99999 or abs(n.q) > 99999:
                    n = sp.Rational(n.p // 10, n.q)
            return n

        def limit_expr(expr):
            """Limit numbers inside an expression to max 5 digits and simplify."""
            # Convert plain Python numbers to SymPy
            expr = sp.sympify(expr)
            # Safely iterate over numeric atoms
            for atom in list(expr.atoms(sp.Integer, sp.Float, sp.Rational)):
                new_val = clean_num(atom)
                if new_val != atom:
                    expr = expr.xreplace({atom: new_val})
            return sp.simplify(expr)

        # --- create structure ---
        left_side = base ** x
        right_side = rhs_val

        # Apply exponent shift safely
        exp_shift = random.randint(-2, 2)
        if exp_shift != 0:
            left_side = base ** (x + exp_shift)
            try:
                scaled = rhs_val * (base ** exp_shift)
                if abs(scaled) > 99999:
                    scaled = scaled / random.randint(20, 100)
                right_side = clean_num(scaled)
            except OverflowError:
                right_side = rhs_val

        # Random arithmetic modifications
        operations = random.sample([add, sub, mul, nmul, truediv, ndiv], k=random.randint(1, 3))
        for func in operations:
            n = clean_num(random.uniform(0.5, 8))
            side = random.choice(['left', 'right', 'both'])
            if side == 'both':
                left_side = func(left_side, n)
                right_side = func(right_side, n)
            elif side == 'left':
                left_side = func(left_side, n)
            else:
                right_side = func(right_side, n)

        # Occasionally scale both sides
        if random.choice([True, False]):
            k = clean_num(random.uniform(0.5, 3))
            left_side = k * left_side
            right_side = k * right_side

        # Clean up expressions to remove large or messy numbers
        left_side = limit_expr(left_side)
        right_side = limit_expr(right_side)

        # Final normalization — if any side still too big, scale down
        for side in [left_side, right_side]:
            for atom in side.atoms(sp.Integer):
                if abs(atom) > 99999:
                    scale = random.randint(50, 500)
                    left_side /= scale
                    right_side /= scale
                    break

        eq = sp.Eq(sp.simplify(left_side), sp.simplify(right_side))
        return eq


    def solving_steps(self):
        return []

    
        



















# cemetery


    #     self.left_side = left_side
    #     self.right_side = right_side
    #     self.roots = roots

    #     self.equation = self.create()
    #     return self.equation

    # def create(self):
    #     changes = [self.complex_exp, self.coef_to_power, self.one_to_exp_zero, self.neg_exponent, self.dec_coef, self.other_side]
    #     for change in changes:
    #         change()
    #     return self.equation
    
    # def complex_exp(self):
    #     for coef in self.left_side:
    #         if coef is str:
    #             continue

    #         num_a = coef[0]
    #         sign = coef[1]
    #         num_b = coef[2]
    #         exp = coef[3]

    #         if sign is not None and num_b is not None and exp is int:
    #             number = sign(num_a, num_b) ** exp
    #         elif exp is int:
    #             number = num_a ** exp
    #         else:
    #             number = num_a



    #     numbers = random.choice(['both_fractions', 'one_fraction', 'both_integers'])
    #     x = sp.symbols('x')
    #     if numbers == 'both_fractions':
    #         numerator_left = random.randint(1, 11)
    #         numerator_right = random.randint(1, 11)
    #         denominator_left = random.randint(1, 11)
    #         denominator_right = random.randint(1, 11)

    #         number_left = sp.symbols(f'{numerator_left}/{denominator_left}')
    #         number_right = sp.symbols(f'{numerator_right}/{denominator_right}')

    #         val_number_left = numerator_left/denominator_left
    #         val_number_right = numerator_right/denominator_right

    #         if self.level == 'advanced':
    #             eq = AdvancedEquation([[numerator_left, '/', denominator_left, x]], [[numerator_right, '/', denominator_right, 1]], [val_x])

    #     elif numbers == 'one_fraction':
    #         numerator_left = random.randint(1, 11)
    #         denominator_left = random.randint(1, 11)
    #         number_right = random.randint(1, 11)

    #         number_left = sp.symbols(f'{numerator_left}/{denominator_left}')
    #         val_number_left = numerator_left/denominator_left
    #         val_number_right = number_right

    #         if self.level == 'advanced':
    #             eq = AdvancedEquation([[numerator_left, '/', denominator_left, x]], [[number_right, '/', 1, 1]], [val_x])
    #     else:
    #         number_right = random.randint(1, 11)
    #         number_left = random.randint(1, 11)
    #         val_number_left = number_left
    #         val_number_right = number_right

    #         if self.level == 'advanced':
    #             eq = AdvancedEquation([[number_left, '/', 1, x]], [[number_right, '/', 1, 1]], [val_x])
            
    #    # define logarythm of both sies first


# def neg_exponent(self, coef):
#         if coef == self.val_a:
#             self.val_a = ((1/self.val_a) ** -1)
#         elif coef == self.val_b:
#             self.val_b = ((1/self.val_b) ** -1)
#         elif coef == self.val_c:
#             self.val_c = ((1/self.val_c) ** -1)
#         else:
#             self.val_r = ((1/self.val_r) ** -1)

#     def dec_coef(self, coef):
#         n = random.randint(1, 10)
        
#         if coef == self.val_a:
#             self.val_a = (self.val_a - n) + n
#         elif coef == self.val_b:
#             self.val_b = (self.val_b - n) + n
#         elif coef == self.val_c:
#             self.val_c = (self.val_c - n) + n
#         else:
#             self.val_r = (self.val_r - n) + n

#     def other_side(self, coef): # ###
#         pass

#     def coef_to_power(self, coef):# only for special cases
#         if int(sqrt(coef)) == sqrt(coef):
#             if coef == self.val_a:
#                 self.val_a = int(sqrt(coef)) ** 2
#             elif coef == self.val_b:
#                 self.val_b = int(sqrt(coef)) ** 2
#             elif coef == self.val_c:
#                 self.val_c = int(sqrt(coef)) ** 2
                
#         elif int(sqrt(coef, 3)) == sqrt(coef, 3):
#             if coef == self.val_a:
#                 self.val_a = int(sqrt(coef)) ** 3
#             elif coef == self.val_b:
#                 self.val_b = int(sqrt(coef)) ** 3
#             elif coef == self.val_c:
#                 self.val_c = int(sqrt(coef)) ** 3
    

#     def complex_exp(self, coef):# only for special cases
         
            

#     def one_to_exp_zero(self, coef):
#         if coef == 1:
#             if coef == self.val_a:
#                 self.val_a = self.val_r ** 0
#             elif coef == self.val_b:
#                 self.val_b = self.val_r ** 0
#             elif coef == self.val_c:
#                 self.val_c = self.val_r ** 0
#         else:
#             pass
            

