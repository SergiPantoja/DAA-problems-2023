from logic import logic
from satisfying import satisfying_converter
import random as rd
import numpy as np

def generator():
    clauses = rd.randint(10, 15)
    variables = rd.randint(3, 5)
    var = create_variables(variables)
    var = assign_values(var)
    formula = []
    
    for i in range(clauses):
        c = list(rd.sample(var, 3))
        formula.append(c)
    return formula

def create_variables(variables):
    vars = []
    for i in range(65, 65 + variables):
        vars.append(chr(i))
    return vars

def assign_values(var):
    vars = []
    for i in var:
        x = rd.randint(0, 1)
        vars.append(logic(i, x))
    return vars

def save_npy():
    cases = []
    solutions = []
    for i in range(10000):
        x = generator()
        y = satisfying_converter(x)
        cases.append(x)
        if(y != None):
            solutions.append(True)
        else:
            solutions.append(False)
    arr = np.asanyarray(cases, dtype=object)
    arr2 = np.asanyarray(solutions, dtype=object)
    np.save('TestCases/test', arr)
    np.save('TestCases/solutions', arr2)

save_npy()
