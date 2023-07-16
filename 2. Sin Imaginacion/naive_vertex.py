from itertools import combinations

def naive_vertex(U: list[int], V: list[int], adj_list: dict) -> list[list[dict]]: #O(2^n * E * k * V)
    total_vertex = U.copy()
    total_vertex.extend(V)
    combs = _combinations(total_vertex)
    min_degree = _min_graph_degree(adj_list)
    
    min_vertex = [99999] * (min_degree + 1)
    best_adj_list = [[]] * (min_degree + 1)
    count = 0
    for i in list(combs):
        subgraph = _create_subgraph(i, adj_list)
        for k in range(min_degree + 1):          
            md =  _min_graph_degree(subgraph)
            if len(i) < min_vertex[k] and md >= k:
                min_vertex[k] = len(subgraph)
                best_adj_list[k] = [subgraph]
            elif len(i) == min_vertex[k] and md >= k:
                best_adj_list[k].append(subgraph)
                
    return best_adj_list
    
def _combinations(total_vertex: list[int]) -> list:  #O(2^n)
    comb = []
    res = []
    for i in range(len(total_vertex)):
        comb.append(combinations(total_vertex, i+1))
    for i in list(comb):
        for j in i:
            res.append(j)
    return res

def _create_subgraph(vertex: list[int], adj_list: dict) -> dict: #O(E)
    new_adj_list = {}
    for i in vertex:
        for j in adj_list[i]:
                if j in vertex and j != i:
                    if(i not in new_adj_list):
                        new_adj_list[i] = []
                    new_adj_list[i].append(j)
    return new_adj_list

def _min_graph_degree(adj_list: dict) -> int: #O(V)
    min = 99999
    if len(adj_list) == 0:
        return 0
    for i in adj_list:
        if len(adj_list[i]) < min:
            min = len(adj_list[i])
    return min