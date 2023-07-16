import numpy as np
from logic import logic
from reduction import an2

def tester():
    t = np.load('TestCases/test.npy', allow_pickle=True)
    s = np.load('TestCases/solutions.npy', allow_pickle=True)
    
    for i in range(len(t)):
        res = an2(t[i])
        if(res == s[i]):
            print('OK')
        else:
            break

tester()