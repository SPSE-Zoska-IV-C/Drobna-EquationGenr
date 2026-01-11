from math_engine.functions.root import Function
import sympy as sp
import random
import numpy as np
import matplotlib.pyplot as plt
import io
from scipy.optimize import brentq


class Exponential(Function):
    def __init__(self, coefficients=None):
        super().__init__(coefficients)
        self.type = 'exponential'

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
                                 'val_bn': self.val_r, 
                                 'val_bd': 1, 
                                 'val_v': self.sum_exp,
                                 'val_n': self.mul_exp,
                                 'val_k': self.sum_base,  
                                 'val_px': (sp.log((0 - self.sum_base)/self.mul_base, self.val_r) - self.sum_exp) /self.mul_exp if -self.sum_base > 0 else None,
                                 'val_py': self.mul_base*(self.val_r**(self.sum_exp)) + self.sum_base})

        if isinstance(self.val_r, sp.Rational):
            self.coefficients.update({'val_bn': self.val_r.numerator, 
                                      'val_bd': self.val_r.denominator})
        
        # a*b**x + k

    def get_parameters(self):
        self.parameters = dict()
        self.parameters.update({
                                'D(f)': ('minus infinity', 'infinity'),
                                'H(f)': (0 + self.coefficients['val_k'], 'infinity'),
                                'Px': (self.coefficients['val_px'], 0),
                                'Py': (0, self.coefficients['val_py']),
                                'parity': 'none',
                                'boundaries': (0 + self.coefficients['val_k'], None), 
                                'monotony': 'decreasing' if self.coefficients['val_bd'] != 1 else 'increasing',
                                'symetheticity': 'asymetric'})
        return self.parameters
    
    
    # def get_graph(self):
    #     # Base
    #     b = self.coefficients['val_bn'] / self.coefficients['val_bd']
    #     a = self.coefficients['val_a']
    #     n = self.coefficients['val_n']
    #     v = self.coefficients['val_v']
    #     k = self.coefficients['val_k']

    #     # Function
    #     f = lambda x: a * b**(n*x + v) + k

    #     # ---- Maximum curvature (correct formula) ----
    #     C = a * n * np.log(b)
    #     u = 1 / (np.sqrt(2) * C)
    #     x_bend = (np.log(u) / np.log(b) - v) / n

    #     # ---- Adjusted x range ----
    #     x_start = x_bend - b
    #     x_end   = x_bend + b
    #     x = np.linspace(x_start, x_end, 400)

    #     # ---- Plot ----
    #     fig, ax = plt.subplots(figsize=(8, 5))
    #     ax.plot(x, f(x), label=rf'$ {self.get_latex_formula()} $')

    #     ax.set_xlabel('x')
    #     ax.set_ylabel('f(x)')
    #     ax.set_title('Exponential Function')
    #     ax.grid(True)
    #     ax.legend()

    #     self.graph = fig
    #     return self.graph

    def get_graph(self):

        a = self.coefficients['val_a']
        b = self.coefficients['val_bn'] / self.coefficients['val_bd']
        n = self.coefficients['val_n']
        v = self.coefficients['val_v']
        k = self.coefficients['val_k']

        def f(x):
            return k + a * b**(n*x + v)
        
        x_min = (-6 - v) / n
        x_max = ( 6 - v) / n
        x_min, x_max = min(x_min, x_max), max(x_min, x_max)
        x = np.linspace(x_min, x_max, 300)

        y = f(x)

        # Domain safety
        mask1 = np.isfinite(x)

        x = x[mask1]
        y = y[mask1]
        
        # print(x)
        # print(y)
        # print(y_inv)

        # print('*********************************************************************')
        # print(x, y)
        # print(type(x), type(y))
        # print('*********************************************************************')

        return x, y, y, x
    
    def get_inverse(self):
        self.inverse_coefficients = self.coefficients
        self.inverse_coefficients.update({'val_px': self.coefficients['val_py'],
                                          'val_py': self.coefficients['val_px']})
        return Logarithmic(self.inverse_coefficients)
    
    def get_latex_formula(self):
        x = sp.symbols('x')

        a  = sp.Rational(self.coefficients['val_a']).limit_denominator(100000)
        k  = sp.Rational(self.coefficients['val_k']).limit_denominator(100000)
        bn = sp.Rational(self.coefficients['val_bn']).limit_denominator(100000)
        bd = sp.Rational(self.coefficients['val_bd']).limit_denominator(100000)
        v  = sp.Rational(self.coefficients['val_v']).limit_denominator(100000)
        n  = sp.Rational(self.coefficients['val_n']).limit_denominator(100000)

        base = bn / bd

        expr = a * (base**(n*x + v)) + k

        return f"f(x) = {sp.latex(expr, fold_func_brackets=True)}"
    
    def plot(self, ax, **kwargs):
        fig = self.get_graph()
        src_ax = fig.axes[0]
        for line in src_ax.get_lines():
            ax.plot(line.get_xdata(), line.get_ydata(), **kwargs)
        plt.close(fig)




# (Logb((X – k)/a) – v) /n
# log b ((X – k)/a)
## use plotly for graphs

class Logarithmic(Function):
    def __init__(self, coefficients=None):
        super().__init__(coefficients)
        self.type = 'logarithmic'

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
                                  'val_bn': self.val_r,
                                  'val_bd': 1,
                                  'val_k': self.sum_base,
                                  'val_v': self.sum_exp,
                                  'val_n': self.mul_exp,
                                  'val_px': ((self.val_r**(0 + self.sum_exp))*self.mul_base) + self.sum_base,
                                  'val_py': (sp.log((0 - self.sum_base)/self.mul_base, self.val_r) - self.sum_exp) /self.mul_exp if -self.sum_base > 0 else None})

        if isinstance(self.val_r, sp.Rational):
            self.coefficients.update({'val_bn': self.val_r.numerator, 
                                      'val_bd': self.val_r.denominator})
        
    def get_parameters(self):
        self.parameters = dict()
        self.parameters.update({
                                'D(f)': (0 + self.coefficients['val_k'], 'infinity'),
                                'H(f)': ('minus infinity', 'infinity'),
                                'Px': (self.coefficients['val_px'], 0),
                                'Py': (0, self.coefficients['val_py']),
                                'parity': 'none',
                                'boundaries': (None, None), 
                                'monotony': 'decreasing' if self.coefficients['val_bd'] != 1 else 'increasing',
                                'symetheticity': 'asymetric'})

        return self.parameters
    
    def get_graph(self):

        a = self.coefficients['val_a']
        b = self.coefficients['val_bn'] / self.coefficients['val_bd']
        n = self.coefficients['val_n']
        v = self.coefficients['val_v']
        k = self.coefficients['val_k']


        def f(x):
            return ((np.log((x - k) / a) / np.log(b)) - v) / n
        

        x_min = (b**(-6) + k) * a
        x_max = (b**(6) + k) * a
        x_min, x_max = min(x_min, x_max), max(x_min, x_max)
        x = np.linspace(x_min, x_max, 300)

        y = f(x)
        

        # Domain safety
        mask1 = np.isfinite(x)

        x = x[mask1]
        y = y[mask1]

        # print('*********************************************************************')
        # print(x, y)
        # print(type(x), type(y))
        # print('*********************************************************************')

        return x, y, y, x
        

        



    # def get_graph(self):

    #     a = self.coefficients['val_a']
    #     b = self.coefficients['val_bn'] / self.coefficients['val_bd']
    #     n = self.coefficients['val_n']
    #     v = self.coefficients['val_v']
    #     k = self.coefficients['val_k']

    #     if b <= 0 or b == 1:
    #         raise ValueError("Invalid logarithm base")

    #     def f(x):
    #         return (np.log((x - k) / a) / np.log(b) - v) / n

    #     def f_inv(y):
    #         return k + a * b**(n*y + v)

    #     # ---------- MAIN BEND (y-based) ----------
        # y_min = (-3 - v) / n
        # y_max = ( 3 - v) / n
        # y = np.linspace(y_min, y_max, 600)

        # x = f_inv(y)

        # # Domain safety
        # mask = np.isfinite(x)
        # x = x[mask]
        # y = y[mask]

    #     # ---------- Intersection with y = x ----------

    #     intersections = []
    #     try:
    #         root = brentq(lambda t: f(t) - t, x.min(), x.max())
    #         intersections.append(root)
    #     except ValueError:
    #         pass

    #     # ---------- Axis limits ----------
    #     all_vals = np.concatenate([x, y])

    #     if intersections:
    #         all_vals = np.concatenate([all_vals, intersections])

    #     lo, hi = all_vals.min(), all_vals.max()
    #     pad = 0.15 * (hi - lo)
    #     lo -= pad
    #     hi += pad

    #     # ---------- Plot ----------
    #     fig, ax = plt.subplots(figsize=(8, 5))

    #     ax.plot(x, y, label='original')
    #     ax.plot(y, x, label='inverse')

    #     for xi in intersections:
    #         ax.plot(xi, xi, 'ro')

    #     ax.axvline(k, linestyle='--', alpha=0.5)
    #     ax.set_xlim(lo, hi)
    #     ax.set_ylim(lo, hi)
    #     ax.set_aspect('equal', adjustable='box')
    #     ax.grid(True)
    #     ax.legend()

    #     return fig, ax


    # def get_graph(self):
    #     a = self.coefficients['val_a']
    #     b = self.coefficients['val_bn'] / self.coefficients['val_bd']
    #     n = self.coefficients['val_n']
    #     v = self.coefficients['val_v']
    #     k = self.coefficients['val_k']


    #     f = lambda x: (np.log((x - k) / a) / np.log(b) - v) / n
    #     f1 = lambda x: a*b**(n*x + v) + k

    #     x_min, x_max = -10-k, 10-k
    #     x = np.linspace(x_min, x_max, 400)
    #     y = f1(x)

    #     fig, ax = plt.subplots(figsize=(8, 5))
    #     ax.plot(x, y, label='inverse')
    #     ax.plot(y, x, label='original')

    #     ax.axvline(k, linestyle='--', alpha=0.5)
    #     ax.grid(True)
    #     ax.set_aspect('equal', adjustable='box')
    #     ax.legend()

    #     return fig, ax





    def get_inverse(self):
        self.inverse_coefficients = self.coefficients
        self.inverse_coefficients.update({'val_px': self.coefficients['val_py'],
                                          'val_py': self.coefficients['val_px']})
        return Exponential(self.inverse_coefficients)
    

    def get_latex_formula(self):
        x = sp.symbols('x')

        a  = sp.Rational(self.coefficients['val_a']).limit_denominator(100000)
        k  = sp.Rational(self.coefficients['val_k']).limit_denominator(100000)
        bn = sp.Rational(self.coefficients['val_bn']).limit_denominator(100000)
        bd = sp.Rational(self.coefficients['val_bd']).limit_denominator(100000)
        v  = sp.Rational(self.coefficients['val_v']).limit_denominator(100000)
        n  = sp.Rational(self.coefficients['val_n']).limit_denominator(100000)

        base = bn / bd

        expr = (
            (sp.log((x - k) / a, 10, evaluate=False))/sp.log(base, 10, evaluate=False) - v
        ) / n

        return f"f(x) = {sp.latex(expr, fold_func_brackets=True)}"
    

    # def plot(self, **kwargs):
    #     fig, ax = self.get_graph()
    #     # fig.savefig("app/static/img-1.png")
    #     # plt.close(fig)

    #     # Create in-memory bytes buffer
    #     img = io.BytesIO()
    #     fig.savefig(img, format='png', bbox_inches='tight')
    #     plt.close(fig)

    #     img.seek(0)  # rewind buffer
    #     return img



