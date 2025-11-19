from equations.exponential import *


def test_substitution():
    method = Substitution('advanced')
    print(method.equation)
    print(method.roots)
    print(method.steps)

def test_matching_bases():
    method = Matching_bases('advanced')
    print(method.equation)
    print(method.roots)
    print(method.steps)

def test_logarithm():
    method = Logarithm('advanced')
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
for i in range(500):
    test_logarithm()
    print('---')


