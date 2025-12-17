from functions.root import Function
import sympy as sp
import random

# log b ((X – k)/a)

class Logarithmic(Function):
    def create_coefficients(self):
        self.coefficients = dict()
        type = random.choices([1, 2, 3, 4, 5], k=random.randint(1, 5))
        self.val_r = random.randint(2, 10) if random.choice([True, False]) else sp.Rational(1/random.randint(2, 10)).limit_denominator(1000)
        self.sum_base, self.sum_exp = 0, 0
        self.mul_base, self.mul_exp = 1, 1
        if 2 in type:
            self.sum_base = random.randint(2, 5)
        if 3 in type:
            self.mul_base = random.choice([i for i in range(2, 5) if i != 3])
        if 4 in type:
            self.sum_exp = random.randint(2, 5)
        if 5 in type:
            self.mul_exp = random.randint(2, 5)

        self.coefficients.update({'val_a': self.mul_base,
                                  'val_b': self.val_r,
                                  'val_k': self.sum_base,
                                  'val_v': self.sum_exp,
                                  'val_n': self.mul_exp,
                                  'val_px': ((self.val_r**(0 + self.sum_exp))*self.mul_base) + self.sum_base,
                                  'val_py': (sp.log((0 - self.sum_base)/self.mul_base, self.val_r) - self.sum_exp) /self.mul_exp if -self.sum_base > 0 else None})
        
        print ('sending into init:', self.coefficients)
        return self.coefficients


    # (Logb((X – k)/a) – v) /n
    def get_parameters(self):
        self.parameters = dict()
        self.parameters.update({'formula': sp.Eq(sp.symbols('f(x)'),(sp.log((sp.symbols('x') - self.coefficients['val_k'])/self.coefficients['val_a'], self.coefficients['val_b']) - self.coefficients['val_v']) / self.coefficients['val_n']),
                                'D(f)': (0 + self.coefficients['val_k'], 'infinity'),
                                'H(f)': ('minus infinity', 'infinity'),
                                'Px': (self.coefficients['val_px'], 0),
                                'Py': (0, self.coefficients['val_py']),
                                'parity': 'none',
                                'boundaries': (None, None), 
                                'monotony': 'decreasing' if self.coefficients['val_b'] < 1 else 'increasing',
                                'symetheticity': 'asymetric'})
        
        print(self.parameters) 

    def create_graph(self):
        pass

    def get_inverse(self):
        pass

if __name__ == '__main__':
    import math_engine.test as test
    for i in range(5):
        test.test_mixed_methods_logarithm()
        print('---')

    print('*********************************************************************')
    for i in range(5):
        test.test_substitution_logarithm()
        print('---')