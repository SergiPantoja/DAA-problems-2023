import sympy
from logic import logic
from satisfying import satisfying_converter
    
def encode(logic_formula, primes):
    mark = []
    encoded = {}
    index = 0
    for i in logic_formula:
        for j in i:
            if(j.var not in mark):
                encoded[j.var] = primes[index]
                index += 1
                mark.append(j.var)
    return encoded

def solve(encoded, logic_formula, mul):
    solutions = simultaneous_congruences(encoded, logic_formula)
    inc = []
    for i in solutions:
        inc.append((i, mul))
    return simultaneous_incongruences(inc)

def simultaneous_congruences(encoded, logic_formula):
    solutions = []
    for i in logic_formula:
        b = []
        n = []
        for j in i:
            b.append(j.val)
            n.append(encoded[j.var])
        solutions.append(chinese_reminder_theorem(b, n))
    return solutions

def chinese_reminder_theorem(a, m):
    M = 1
    for mi in m:
        M *= mi
    
    Mi = [M // mi for mi in m]
    
    mult_inverse = [pow(Mi[i], -1, m[i]) for i in range(len(m))]
    
    x = sum(a[i] * Mi[i] * mult_inverse[i] for i in range(len(m))) % M
    
    return x

def simultaneous_incongruences(inc):
    flag = True
    for i in range(10000000000):
        for j in inc:
            if((i - j[0]) % j[1] == 0):
                flag = True
                break
            else:
                flag = False
        if(not flag):
            return True
    return False

def an2(logic_formula):

    primes = list(sympy.primerange(0, 1000))
    
    enc = encode(logic_formula, primes)
    n = 1
    for i in enc:
        n *= enc[i]
    
    return solve(enc, logic_formula, n)
    # if(type(res) == int and type(sat) != None):
    #     print(True)
    # else:
    #     print(False)