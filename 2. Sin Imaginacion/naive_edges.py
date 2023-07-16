from itertools import combinations

def naive_edges(U: list[int], V: list[int], adj_list: dict) -> list[list[dict]]: #O(2^n * E * k * V)

    vertex = len(U) + len(V)
    combs = _combinations(adj_list)
    min_degree = _min_graph_degree(adj_list, vertex)
    
    min_edges = [99999] * (min_degree + 1)
    best_adj_list = [[]] * (min_degree + 1)

    for i in list(combs):
        subgraph = _create_subgraph(i, adj_list)
        for k in range(min_degree + 1): 
            md =  _min_graph_degree(subgraph, vertex)

            if len(i) < min_edges[k] and md >= k:
                min_edges[k] = len(i)
                best_adj_list[k] = [i]
            elif len(i) == min_edges[k] and md >= k:
                best_adj_list[k].append(i)
                
    return best_adj_list
    
def _combinations(adj_list: list[int]) -> list:  #O(2^n)
    edges = _get_edges(adj_list)
    comb = []
    res = []
    for i in range(len(edges) + 1):
        comb.append(combinations(edges, i))
    for i in list(comb):
        for j in i:
            res.append(j)
    return res

def _min_graph_degree(subgraph: dict, vertex: dict) -> int: #O(V)
    min = 99999
    
    if len(subgraph) == 0 or len(subgraph) != vertex:
        return 0
    for i in subgraph:
        if len(subgraph[i]) < min:
            min = len(subgraph[i])
    return min

def _get_edges(adj_list: dict) -> list: #O(E)
    edges = []
    for i in adj_list:
        for j in adj_list[i]:
            edges.append((i, j))
    return edges

def _create_subgraph(edges: list[int], adj_list: dict) -> dict: #O(E)
    new_adj_list = {}
    for i in edges:
        if(i[0] not in new_adj_list):
            new_adj_list[i[0]] = []
        new_adj_list[i[0]].append(i[1])
        if(i[1] not in new_adj_list):
            new_adj_list[i[1]] = []
        new_adj_list[i[1]].append(i[0])
    return new_adj_list