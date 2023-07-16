from itertools import combinations

def naive_vertex_prunning(U: list[int], V: list[int], adj_list: dict) -> list[dict]: #O(logV * (n, logV) * E * V * k)
    total_vertex = U.copy()
    total_vertex.extend(V)
    min_degree = _min_graph_degree(adj_list)
    
    min_vertex = [99999] * (min_degree + 1)
    best_adj_list = []
    memo = {}
    
    for k in range(min_degree + 1):
        result, memo = binary_search(total_vertex, min_vertex, adj_list, k, memo)
        best_adj_list.append(result)
    
    return best_adj_list
    
    
def _combinations(total_vertex: list[int], mid: int) -> list:
    res = []
    combs = combinations(total_vertex, mid)
    for i in list(combs):
        res.append(i)
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

def binary_search(total_vertex: list[int], min_vertex: list[int], adj_list: dict, k: int, memo: dict) -> dict: #O(logV * (n, logV) * E * V)

    left = k * 2
    right = len(total_vertex) - 1 if len(total_vertex) % 2 != 0 else len(total_vertex)
    
    while left < right:
        mid = (left + right) // 2
        mid = mid - 1 if mid % 2 != 0 else mid

        if mid not in memo:
            combs = _combinations(total_vertex, mid)
            memo[mid] = combs
        else:
            combs = memo[mid]
            
        current_adj_list = {}
        
        for i in list(combs):
            subgraph = _create_subgraph(i, adj_list)             
            if len(i) < min_vertex[k] and _min_graph_degree(subgraph) >= k:
                min_vertex[k] = len(subgraph)
                current_adj_list = subgraph

        if min_vertex[k] == k * 2:
            return current_adj_list, memo
        elif min_vertex[k] != 99999:
            right = mid
        else:
            left = mid + 2
    
    return current_adj_list, memo 