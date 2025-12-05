from functions.root import Function
import sympy as sp
import random



class Exponential(Function):
    def create_coefficiens(self):
        self.coefficiens = dict()
        type = random.choices([1, 2, 3, 4, 5], k=random.randint(1, 5))
        self.val_r = random.randint(2, 10) if random.choice([True, False]) else sp.Rational(1/random.randint(2, 10)).limit_denominator(1000)
        sum_base, sum_exp = 0, 0
        mul_base, mul_exp = 1, 1
        if 2 in type:
            sum_base = random.randint(-2, 5)
        if 3 in type:
            mul_base = random.randint(2, 5)
        if 4 in type:
            sum_exp = random.randint(2, 5)
        if 5 in type:
            mul_exp = random.randint(2, 5)
        
        
        self.coefficiens.update({'val_a': mul_base, 
                                 'val_bx': self.val_r**(mul_exp*sp.symbols('x') + sum_exp), 
                                 'val_k': sum_base, 
                                 'dec_poss': True, 
                                 'val_px': (sp.log(sp.Rational(-(sum_base/mul_base)).limit_denominator(1000), self.val_r) - sum_exp)/mul_exp if -(sum_base/mul_base) > 0 else None,
                                 'val_py': mul_base*(self.val_r**(sum_exp)) + sum_base})
        print('vytvorene ',self.coefficiens)

        return self.coefficiens
        # a*b**x + k

    def get_parameters(self):
        self.parameters = dict()
        print('prevzate ',self.coefficiens)
        eq = sp.Eq(self.coefficiens['val_a'] * self.coefficiens['val_bx'] + self.coefficiens['val_k'], sp.symbols('y'))
        self.parameters.update({'formula': sp.Eq(sp.symbols('f(x)'), self.coefficiens['val_a'] * self.coefficiens['val_bx'] + self.coefficiens['val_k']),
                                'D(f)': ('minus infinity', 'infinity'),
                                'H(f)': (0 + self.coefficiens['val_k'], 'infinity'),
                                'Px': (self.coefficiens['val_px'], 0),
                                'Py': (0, self.coefficiens['val_py']),
                                'parity': 'none',
                                'boundaries': (0 + self.coefficiens['val_k'], None), 
                                'monotony': 'decreasing' if 'dec_poss' in self.coefficiens and self.val_r < 1 else 'increasing',
                                'symetheticity': 'asymetric'})
        


        
    def create_graph(self):
        pass