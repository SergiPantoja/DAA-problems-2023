from ast import literal_eval
from naive_vertex_prunning import naive_vertex_prunning
from dinic_edges import optimal_d

def _load_txt():
    test = []
    sol = []
    with open("TestCases/tests.txt") as f:
        for line in f:
            parsed_s = literal_eval('[' + line + ']')
            test.append(parsed_s)
    with open("TestCases/solutions.txt") as f:
        a = []
        for line in f:
            parsed_s = literal_eval(line)
            sol.append(parsed_s)
    return test, sol

def tester():
    test, sol = _load_txt()
    for i in range(len(test)):
        res = naive_vertex_prunning(test[i][0], test[i][1],test[i][2])
        flag = False
        for j in range(len(res)):
            if res[j] not in sol[i][j]:
                print(f'Case {i}: Wrong')
                flag = True
        if(not flag):
            print(f'Case {i}: ok')
    
tester()