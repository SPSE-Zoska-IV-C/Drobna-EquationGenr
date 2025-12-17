import equations.logarithmic as log
import equations.exponential as ex
import functions.exponential as func_ex
import functions.logarithmic as func_log

### Logarithms ###
def test_mixed_methods_logarithm():
    method = log.Mixed_methods('advanced')
    print(method.equation)
    print(method.roots)
    print(method.steps)
    method.create_function_coefficients()
    print(method.func_coefs)
    func_log.Logarithmic(method.func_coefs).get_parameters()

def test_substitution_logarithm():
    method = log.Substitution('simple')
    print(method.equation)
    print(method.roots)
    print(method.steps)
    method.create_function_coefficients()
    print(method.func_coefs)
    func_log.Logarithmic(method.func_coefs).get_parameters()

### Exponentials ###

def test_substitution_exponential():
    method = ex.Substitution('advanced')
    print(method.equation)
    print(method.roots)
    print(method.steps)
    method.create_function_coefficients()
    print(method.func_coefs)
    func_ex.Exponential(method.func_coefs).get_inverse().get_parameters()

def test_matching_bases_exponential():
    method = ex.Matching_bases('advanced')
    print(method.equation)
    print(method.roots)
    print(method.steps)
    method.create_function_coefficients()
    print(method.func_coefs)
    func_ex.Exponential(method.func_coefs).get_inverse().get_parameters()

def test_logarithm_exponential():
    method = ex.Logarithm('advanced')
    print(method.equation) 
    print(method.roots)
    print(method.steps)
    method.create_function_coefficients()
    print(method.func_coefs)
    func_ex.Exponential(method.func_coefs).get_inverse().get_parameters()


for i in range(50):
    test_mixed_methods_logarithm()
    print('---')

# print('*********************************************************************')
# for i in range(5):
#     test_substitution_logarithm()
#     print('---')


############################################################################### 

# for i in range(50): 
#     test_substitution_exponential()
#     print('---')
    

# print('*********************************************************************')
# for i in range(50):
#     test_matching_bases_exponential()
#     print('---')


# print('*********************************************************************')
# for i in range(50):
#     test_logarithm_exponential()
#     print('---')


