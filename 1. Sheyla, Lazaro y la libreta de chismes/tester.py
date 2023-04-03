from optimal import optimal

def LoadTxt():
    test = []
    sol = []
    with open("TestCases/tests.txt") as f:
        for line in f:
            test.append(line.split(','))      
    with open("TestCases/solutions.txt") as f:
        for line in f:
            sol.append(line)
    return test, sol

def Tester():
    test, sol = LoadTxt()
    for i in range(len(test)):
        res = optimal(list(test[i][0:len(test[i])-1]))
        if(res == int(sol[i])):
            print(f'Case {i}: OK')
        else:
            print(f'Case {i}: Wrong')

Tester()