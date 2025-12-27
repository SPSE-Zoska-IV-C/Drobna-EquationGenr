from functions.root import Function
import sympy as sp
import random



class Exponential(Function):
    def create_coefficients(self):
        self.coefficients = dict()
        type = random.choices([1, 2, 3, 4, 5], k=random.randint(1, 5))
        self.val_r = random.randint(2, 10) if random.choice([True, False]) else sp.Rational(1/random.randint(2, 10)).limit_denominator(1000)
        self.sum_base, self.sum_exp = 0, 0
        self.mul_base, self.mul_exp = 1, 1
        if 2 in type:
            self.sum_base = random.randint(-2, 5)
        if 3 in type:
            self.mul_base = random.randint(2, 5)
        if 4 in type:
            self.sum_exp = random.randint(2, 5)
        if 5 in type:
            self.mul_exp = random.randint(2, 5)
        
        
        self.coefficients.update({'val_a': self.mul_base, 
                                 'val_b': self.val_r, 
                                 'val_v': self.sum_exp,
                                 'val_n': self.mul_exp,
                                 'val_k': self.sum_base,  
                                 'val_px': (sp.log((0 - self.sum_base)/self.mul_base, self.val_r) - self.sum_exp) /self.mul_exp if -self.sum_base > 0 else None,
                                 'val_py': self.mul_base*(self.val_r**(self.sum_exp)) + self.sum_base})

        # a*b**x + k

    def get_parameters(self):
        self.parameters = dict()
        self.parameters.update({'formula': sp.Eq(sp.symbols('f(x)'), self.coefficients['val_a'] * self.coefficients['val_b']**(self.coefficients['val_n']*sp.symbols('x') + self.coefficients['val_v']) + self.coefficients['val_k']),
                                'D(f)': ('minus infinity', 'infinity'),
                                'H(f)': (0 + self.coefficients['val_k'], 'infinity'),
                                'Px': (self.coefficients['val_px'], 0),
                                'Py': (0, self.coefficients['val_py']),
                                'parity': 'none',
                                'boundaries': (0 + self.coefficients['val_k'], None), 
                                'monotony': 'decreasing' if self.coefficients['val_b'] < 1 else 'increasing',
                                'symetheticity': 'asymetric'})
        print(self.parameters)
    
 
    def create_graph(self):
        pass

    def get_inverse(self):
        self.inverse_coefficients = self.coefficients
        self.inverse_coefficients.update({'val_px': self.coefficients['val_py'],
                                          'val_py': self.coefficients['val_px']})
        return Logarithmic(self.inverse_coefficients)
    
# (Logb((X – k)/a) – v) /n
# log b ((X – k)/a)
## use plotly for graphs

class Logarithmic(Function):
    def create_coefficients(self):
        if self.coefficients is not None:
            return
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


    def create_graph(self):
        pass


    # def get_inverse(self):
    #     self.inverse_coefficients = self.coefficients
    #     self.inverse_coefficients.update({'val_px': self.coefficients['val_py'],
    #                                       'val_py': self.coefficients['val_px']})
    #     return Exponential(self.inverse_coefficients)
        
