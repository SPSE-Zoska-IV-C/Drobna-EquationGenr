from equations.exponential import *


def test_substitution(): # working
    method = Substitution('simple')
    print(method.equation)
    print(method.roots)
    print(method.steps)

def test_matching_bases():
    method = Matching_bases('simple')
    print(method.equation)
    print(method.roots)
    print(method.steps)

def test_logarithm():
    method = Logarithm('simple')
    print(method.equation) 
    print(method.roots)
    print(method.steps)

for i in range(50):
    test_substitution()
    print('---')
    

print('*********************************************************************')
for i in range(50):
    test_matching_bases()
    print('---')

print('*********************************************************************')
for i in range(50):
    test_logarithm()
    print('---')


