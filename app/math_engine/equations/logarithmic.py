from root import Method, nmul, ndiv

from operator import sub, add, mul, truediv
import sympy as sp
import random


class Mixed_methods(Method):
    def create(self):
        self.val_r = random.randint(2, 11)  # root of the logarithm
        self.val_log = random.randint(1, 6) # main logarithm of the equation
        self.val_x = self.val_r ** self.val_log

        self.roots = [self.val_x]

        if self.level == 'simple':
            self.create_simple()
        elif self.level == 'advanced':
            self.create_advanced()
    
    
    def create_function_coefficients(self):
        self.func_coefs = [self.val_r, self.val_log]

    def create_simple(self):
        self.equation = sp.Eq(sp.log(sp.symbols('x'), self.val_r), self.val_log)
        self.steps.append(self.equation)


    def create_advanced(self):
        x = sp.symbols("x")
        base = self.val_r
        sol = self.val_x

        required_laws = random.randint(1, 3)

        components = []

        k = random.randint(2, 8)
        comp_product = (
            sp.log(x, base) + sp.log(k, base),
            sp.log(sol, base) + sp.log(k, base),
            {"product"},
        )
        components.append(comp_product)

        m = random.randint(2, 8)
        comp_quotient = (
            sp.log(m * x, base) - sp.log(m, base),
            sp.log(m * sol, base) - sp.log(m, base),
            {"quotient"},
        )
        components.append(comp_quotient)

        c = random.randint(2, 5)
        comp_power = (
            c * sp.log(x, base),
            c * sp.log(sol, base),
            {"power"},
        )
        components.append(comp_power)

        random.shuffle(components)
        chosen_components = components[:required_laws]

        left_expr = chosen_components[0][0]
        right_expr = chosen_components[0][1]

        self.steps.append(sp.Eq(left_expr, right_expr))

        template_type = random.randint(1, 5)

        if template_type == 1:
            if required_laws > 1:
                left_expr += chosen_components[1][0]
                right_expr += chosen_components[1][1]
            if required_laws > 2:
                left_expr -= chosen_components[2][0]
                right_expr -= chosen_components[2][1]

        elif template_type == 2:
            left_expr = sp.log(left_expr, base)
            right_expr = sp.log(right_expr, base)

        elif template_type == 3:
            mult = random.randint(2, 5)
            left_expr = chosen_components[0][0] * mult
            right_expr = chosen_components[0][1] * mult

        elif template_type == 4:
            if required_laws > 1:
                left_expr = sp.log(chosen_components[0][0] + chosen_components[1][0], base)
                right_expr = sp.log(chosen_components[0][1] + chosen_components[1][1], base)

        elif template_type == 5:
            left_expr = sp.log(sp.log(left_expr + k, base), base)
            right_expr = sp.log(sp.log(right_expr + k, base), base)

        self.equation = sp.Eq(left_expr, right_expr)
        self.steps.append(self.equation)


class Substitution(Method):
    def create(self):
        self.val_r = random.randint(2, 11)  # root of the logarithm
        self.val_log1 = random.randint(0, 6) # main logarithm of the equation
        self.val_log2 = random.randint(0, 6) # main logarithm of the equation
        self.val_x1 = self.val_r ** self.val_log1
        self.val_x2 = self.val_r ** self.val_log2


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


