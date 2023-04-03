import random as rd
from naive import Naive

def Generator():
    res = []
    for i in range(100):
        tam = rd.randint(0,20)
        list = []
        for j in range(tam):
            num = rd.randint(1, 8)
            list.append(num)
        res.append(list)
    return res

def SaveTXT():
    f = open("TestCases/tests.txt", "a")
    tc = Generator()
    for i in tc:
        for j in i:
            f.write(f'{j},')
        f.write(f'\n')
    f.close()
    return tc 

def SolveGen():
    tc=SaveTXT()
    f = open("TestCases/solutions.txt", "a")
    for i in tc:
        res=Naive(i)
        if(type(res)==list):
            l = len(res[0])
            f.write(f'{l}\n')
        else:
            f.write(f'{res}\n')

SolveGen()