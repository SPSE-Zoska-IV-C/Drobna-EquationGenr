from logarithmic import *

def test_mixed_methods():
    method = Mixed_methods('simple')
    print(method.equation)
    print(method.roots)
    print(method.steps)

for i in range(50):
    test_mixed_methods()
    print('---')