class Edge:
	def __init__(self, v: int, flow: int, C: int, rev: int):
		self.v = v
		self.flow = flow
		self.C = C
		self.rev = rev

class Graph:
	def __init__(self, V):
		self.adj = [[] for i in range(V)]
		self.V = V
		self.level = [0 for i in range(V)]

	def _add_edge(self, u: int, v: int, C: int):

		a = Edge(v, 0, C, len(self.adj[v]))

		b = Edge(u, 0, 0, len(self.adj[u]))
		self.adj[u].append(a)
		self.adj[v].append(b)

	def _bfs(self, s, t):
		for i in range(self.V):
			self.level[i] = -1

		self.level[s] = 0

		q = []
		q.append(s)
		while q:
			u = q.pop(0)
			for i in range(len(self.adj[u])):
				e = self.adj[u][i]
				if self.level[e.v] < 0 and e.flow < e.C:

					self.level[e.v] = self.level[u]+1
					q.append(e.v)

		return False if self.level[t] < 0 else True

	def _send_flow(self, u: int, flow: int, t: int, start: int):
		if u == t:
			return flow

		while start[u] < len(self.adj[u]):

			e = self.adj[u][start[u]]
			if self.level[e.v] == self.level[u]+1 and e.flow < e.C:

				curr_flow = min(flow, e.C-e.flow)
				temp_flow = self._send_flow(e.v, curr_flow, t, start)

				if temp_flow and temp_flow > 0:
					e.flow += temp_flow
					self.adj[e.v][e.rev].flow -= temp_flow
					return temp_flow
			start[u] += 1

	def _dinic(self, s: int, t: int, U: list[int]):
		if s == t:
			return -1
		total = 0
		while self._bfs(s, t) == True:
			start = [0 for i in range(self.V+1)]
			while True:
				flow = self._send_flow(s, float('inf'), t, start)
				if not flow:
					break
				total += flow   
		solution_edges = []
		for i in U:
			for j in self.adj[i]:
				if(j.flow == 0 and j.v != 0 and j.v != len(self.adj)):
					solution_edges.append((i,j.v))
		return tuple(solution_edges)

def _create_source(U: list[int], in_degree: dict, out_degree: dict):
    out_degree[0] = []
    for i in U:
        in_degree[i] = [0]
        out_degree[0].append(i)
    return in_degree, out_degree, 0    

def _create_target(V: list[int], U: list[int], in_degree: dict, out_degree: dict):
    target = max(max(U), max(V)) + 1
    in_degree[target] = []
    for i in V:
        if(i not in out_degree):
            out_degree[i]=[]
        out_degree[i].append(target)
        in_degree[target].append(i)
    return in_degree, out_degree, target

def _min_graph_degree(adj_list: dict) -> int: #O(V)
    min = 99999
    if len(adj_list) == 0:
        return 0
    for i in adj_list:
        if len(adj_list[i]) < min:
            min = len(adj_list[i])
    return min

def _create_flow(g: Graph, in_degree: dict, out_degree: dict, k: int, target: int, U: list[int], V: list[int]):
    for i in U:
        g._add_edge(0, i, len(out_degree[i]) - k)
        for j in out_degree[i]:
            g._add_edge(i, j, 1)
    for i in V:
        g._add_edge(i, target, len(in_degree[i]) - k) 

def _direct_graph(U: list[int], V: list[int], adj_list: dict):
    in_degree, out_degree = {}, {} 
    for i in adj_list:
        if(i in U):
            out_degree[i] = adj_list[i]
        else:
            in_degree[i] = adj_list[i]
    return out_degree, in_degree

def optimal_d(U: list[int], V: list[int], adj_list: dict):
    out_degree, in_degree = _direct_graph(U, V, adj_list)
    return optimal_dinic(U, V, out_degree, in_degree, adj_list)

def optimal_dinic(U: list[int], V: list[int], out_degree: dict, in_degree: dict, adj_list: dict):
    in_degree, out_degree, source = _create_source(U, in_degree, out_degree)
    in_degree, out_degree, target = _create_target(V, U, in_degree, out_degree)
    min_degree = _min_graph_degree(adj_list)
    solution = []
    for k in range(min_degree + 1):
        g = Graph(len(U + V)+2)
        _create_flow(g, in_degree, out_degree, k, target, U, V)
        solution.append(g._dinic(source, target, U))
    return solution
