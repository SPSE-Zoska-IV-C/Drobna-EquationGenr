from equations import *


def test_substitution(): # working
    method = Substitution('hard')
    print(method.equation)
    print(method.roots)
    # print(sp.solve(method.equation))

def test_matching_bases():
    method = Matching_bases('hard')
    print(method.equation)
    print(method.roots)
    # print(sp.solve(method.equation))

def test_logarithm():
    method = Logarithm('hard')
    print(method.equation) 
    print(method.roots)
    # print(sp.solve(method.equation))

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


