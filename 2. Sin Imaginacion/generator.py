import random as rd
from naive_vertex import naive_vertex
from naive_edges import naive_edges

def _generator() -> tuple[list[int], list[int], dict]:
    U, V, v = _bipartition_generator()
    adj_list = _edges_generator(U, V, v)
    return U, V, adj_list
    
def _bipartition_generator() -> tuple[list[int], list[int], int]:
    v = rd.randint(6, 10)
    U, V = [], []
    for i in range(1, v, 1):
        U.append(i) if rd.randint(0, 1) == 0 else V.append(i)
    return U, V, v

def _edges_generator(U: list[int], V: list[int], v: int) -> dict:
    adj_list = {}
    for i in range(1, v, 1):
        adj_list[i] = []
    for i in U:
        adj_list[i] = rd.sample(V, min(2, len(V)))
        for j in adj_list[i]:
            adj_list[j].append(i)
    return adj_list

def _save_txt() -> list[tuple[list[int], list[int], int]]:
    f = open("TestCases/tests_edges.txt", "a")
    tests = []
    for i in range(5):
        x, y, z = _generator()
        if(len(x) == 0 or len(y) == 0):
            break
        tests.append([x, y, z])
        f.write(f'{x}, {y}, {z} \n')
    f.close()
    return tests 
    
def solve_gen():
    tc = _save_txt()
    f = open("TestCases/solutions_edges.txt", "a")
    for i in tc:
        res=naive_edges(i[0], i[1], i[2])
        f.write(f'{res} \n')

solve_gen()