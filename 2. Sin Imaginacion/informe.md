# Diseño y Análisis de Algoritmos
## Kevin Talavera Díaz - C411
## Sergio Pérez Pantoja - C411

<br>

## Sin imaginación.

Kevin estaba leyendo un libro sobre Diseño y Análisis de Algoritmos cuando se topó con un problema que llamó su atención. El texto era el siguiente:

Se tiene un grafo bipartito $G$ con $U$ nodos en el la primera parte y $V$ nodos en la segunda parte. Un subgrafo de $G$ está k-cubierto si todos sus nodos tienen al menos grado k. Un subgrafo k-cubierto es mínimo si su cantidad de vértices es la mínima posible. Encuentre el mínimo grafo k-cubierto para todo $k$ entre 0 y MinDegree (grado mínimo del grafo $G$).

Luego de entender el problema, automáticamente pensó dos cosas:

- Quiero resolver este problema.

- ¿A los profesores se les abrá acabado la imaginación para los textos de los proyectos?

<br>

## Ejemplo de solución del problema

Sean $U$ y $V$ las dos partes de un grafo $G$ bipartito tales que :

```python
U = [1, 2, 3]
V = [4, 5, 6]
```

Sea la lista de adyacencia de $G$ :

```python
adj_list = {1: [4, 5], 2: [4, 5, 6], 3: [5, 6],
            4: [1, 2], 5: [1, 2, 3], 6: [2, 3]}
```

<br>

Tenemos 3 condiciones que cumplir, de las cuales nos centraremos en las 2 más importantes, y mas adelante será mencionada la tercera:

<br>

- Dado $G$ tenemos que encontrar un subgrafo $G$ $'$ donde $\forall$ v $\in$ $V$ $($ $G$ $'$ $)$ se cumpla que $deg(v)$ $\ge$ $k$

    Tomemos en este caso $k = 2$ :

    $G'_1$ :
    ```python
    U = [1, 2]
    V = [4, 5]
    adj_list = {1: [4, 5], 2: [4, 5],
                4: [1, 2], 5: [1, 2]}
    ```
    $G'_2$ :
    ```python
    U = [2, 3]
    V = [5, 6]
    adj_list = {2: [5, 6], 3: [5, 6],
                5: [2, 3], 6: [2, 3]}
    ```
    $G'_3$ :
    ```python
    U = [1, 2, 3]
    V = [4, 5, 6]
    adj_list = {1: [4, 5], 2: [4, 6], 3: [5, 6],
                4: [1, 2], 5: [1, 3], 6: [2, 3]}
    ```
    $G'_4$ :
    ```python
    U = [1, 2, 3]
    V = [4, 5, 6]
    adj_list = {1: [4, 5], 2: [4, 5, 6], 3: [5, 6],
                4: [1, 2], 5: [1, 2, 3], 6: [2, 3]}
    ```
    Como se puede observar los 4 casos antes expuestos podrían ser una solución válida.

<br>

- El subrafo $G$ $'$ encontrado anteriormente tiene que ser el mínimo posible (con respecto a la cantidad de vértices).

    En este caso la solución es tanto $G'_1$ como $G'_2$, debido a que estos solo contienen 4 vértices y $G'_3$, $G'_4$ tienen 6.

<br>

- Hay que obtener el subgrafo $G$ $'$ mencionado en el punto anterior $\forall$ $k : 0 \le k \le minDegree(G)$
donde $minDegree(G)$ se refiere al grado del vértice con menor grado en $G$.

    En este ejemplo $minDegree(G) = 2$, por tanto las soluciones serían :

    - Para $k = 0$ tomar cualquier $v : v \in V(G)$.
    - Para $k = 1$ tomar cualquier par de vértices $u, v \in V(G) :$ $<u, v> \in E(G)$
    - Para $k = 2$ las anteriormente vistas, $G'_1$ ó $G'_2$

<br>

## Ideas abordadas

### Fuerza Bruta

Esta solución consiste en probar todas las combinaciones de poner y quitar vértices de $G$ y quedarnos con la que cumpla las 3 condiciones mencionadas anteriormente. Esto siempre va a funcionar debido a que se están generando todos los subgrafos posibles y para cada uno se verifica el cumplimiento de las restricciones.

```python
def naive_vertex(U: list[int], V: list[int], adj_list: dict) -> list[list[dict]]:
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
```

La complejidad de este algoritmo es $O(2^V)$ para generar todas las formas de escoger vértices, por cada combinación hay que conectar las aristas correspondientes, si existen, esto es $O(E)$ y luego verificar si todos los vértices tienen al menos grado $k$ en $O(V)$ $\forall k \in minDegree(G)$. La complejidad general de este algoritmo sería: $O(k*E*V*2^V)$.

### Fuerza bruta + Podas

Como el resultado del problema consiste en minimizar la cantidad de vértices y hay una cantidad finita de vértices en $G$, en vez de iterar por cada cantidad desde 1 hasta $|V(G)|$ se puede realizar una búsqueda binaria para agilizar el proceso de la siguiente forma:

- Sean $l = k * 2$, $r = |V(G)|$, $mid = (l + r)/2$ los índices de una búsqueda binaria, $k : 0 \le k \le minDegree(G)$ y $x : 1 \le x \le |V(G)|$ pueden existir 2 casos. Si se econtró solución tomando $x$ vértices para un valor de $k$ se procede a buscar una mejor (realizar la búsqueda desde $l$ a $r = mid$). Si no se encontró solución, tampoco puede existir una con una menor cantidad de vértices, por lo que hay que aumentar esta cantidad y se hace la búsqueda desde $l = mid + 2$ a $r$.

Más adelante será explicado por qué $l = mid + 2$ y por qué se inicializa a $l$ con $k * 2$.


```python
def binary_search(total_vertex: list[int], min_vertex: list[int], adj_list: dict, k: int, memo: dict) -> dict:

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
```

Por otra parte, para $k = 0$ la solución siempre será tomar un vértice, para $k = 1$ es una arista cualquiera de $G$, a partir de $k = 2$ ocurre algo interesante.

- Comenzamos por definir lo que es un grafo k-regular, estos son grafos donde todos sus vértices tienen grado $k$, esto implica que para $k \ge 2$ el grafo siempre va a tener al menos un ciclo.

    - Demostremos que todo grafo 2-regular tiene al menos un ciclo:

        Supongamos que se tenemos un grafo 2-regular sin ciclos. Esto significa que cada vértice del grafo tiene exactamente 2 aristas que lo conectan con otros vértices. Si comenzamos por un vértice arbitrario y seguimos por una de sus aristas, llegaremos a otro vértice. Como el grafo es 2-regular, este también tiene 2 aristas que lo conectan con otros vértices. Sin embargo como estamos suponiendo que el grafo no tiene ciclos, ninguna de estas dos aristas puede llevarnos denuevo al primer vértice. Por lo tanto, debemos seguir avanzando por el grafo, visitando nuevos vértices y siguiendo sus aristas, pero, como el grafo es finito, en algún momento llegaremos a un vértice que ya hemos visitado antes. En este momento tendremos 2 opciones: o seguir avanzando por el grafo, visitando nuevos vértices y siguiendo sus aristas como hicimos al principio, o volvemos sobre nuestro pasos y seguimos la otra arista que conecta el vértice actual con el vértice que ya visitamos antes. En cualquier caso estaremos formando un ciclo en el grafo. Esto es una contradicción con lo supuesto al comienzo de la demostración, por lo que podemos concluir afirmando que todo grafo 2-regular tiene un ciclo.
    
    Luego de obtener este resultado lo podemos extender a cualquier grafo k-regular para $k > 2$, incluso para grafos donde $minDegree(G) = 2$, donde este último caso es el de nuestro ejercicio.

- También se tiene que todo subrafo de un grafo bipartito es también bipartito.

    - Demostración:
    
        Supongamos que tenemos un grafo bipartito $G$ con 2 conjuntos de vértices $A$ y $B$, de tal manera que todas las aristas del grafo conectan un vértice de $A$ con un vértice de $B$. Ahora consideremos cualquier subgrafo $H$ de $G$. Este subgrafo puede tener algunos de los vértices de $A$ y algunos de $B$ pero no necesariamente todos ellos. Para demostrar que $H$ también es bipartito, podemos utilizar el siguiente razonamiento:

        Supongamos que $H$ no es bipartito. Esto significa que existe un ciclo de longitud impar en $H$. Como $H$ es subgrafo de $G$, este ciclo impar también existe en $G$. Sin embargo como $G$ es bipartito, no puede tener ciclos impares. Por lo tanto hemos llegado a un contradicción.

En este punto podemos afirmar que el grafo $G$ bipartito donde $minDegree(G) = 2$, tiene necesariamente que tener ciclos, y estos siempre van a ser de longitud par, por tanto los subgrafos $G'$ de $G$ que pertenezcan a la solución del problema con $k \ge 2$ también van a cumplir esto. Además se deduce que la cantidad de vértices de $G'$ tiene que ser par.

Dicho esto, la búsqueda binaria puede realizarse sobre cantidades pares de vértices y el mínimo de vértices a escoger por cada bipartición es $k$.

```python
def naive_vertex_prunning(U: list[int], V: list[int], adj_list: dict) -> list[dict]:
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
```

La complejidad de este algoritmo sería $O(k*log(V)*E*V*$ $V \choose log(V)$)

### K-Factor

En teoría de grafos existe un término llamado k-factor. Este consiste en extraer un subgrafo $G'$ k-regular de un grafo $G$. Este es un problema muy similar al nuestro pero no funciona debido a que este trabaja de manera general utilizando el algoritmo de emparejamiento máximo $k$ veces, por lo que básicamente trata de obtener un subgrafo k-regular con la mayor cantidad de vértices posibles. Esto es el opuesto de nuestro problema, el cual la idea es bastante simple y no hay forma de abstraerlo a nuestro problema manteniéndolo en tiempo polinomial.

Link del paper que habla en detalle del algoritmo: https://research.cs.queensu.ca/home/daver/Pubs/MyPDF/On_k_Factors_IPL.pdf

## Ejercicio 2

Debido a que no se logró obtener una solución polinomial para este problema, se acordó con los profesores realizar uno con una orientación similar, el cual consiste en encontrar el menor subconjunto de aristas tal que todos los vértices del grafo $G$ bipartito tengan grado $k$ : $0 \le k \le minDegree(G)$.

## Ideas abordadas

### Fuerza bruta

Al igual que en el algoritmo de fuerza bruta del ejercicio 1, esta solución consiste en probar todas las combinaciones de poner y quitar, en este caso aristas de $G$ y quedarnos con la que cumpla las 3 condiciones mencionadas anteriormente. Esto siempre va a funcionar debido a que se están generando todos los subgrafos posibles y para cada uno se verifica el cumplimiento de las restricciones.

```python
def naive_edges(U: list[int], V: list[int], adj_list: dict) -> list[list[dict]]:

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
```

### Óptimo:

Como en este problema tenemos que dejar en $G$ la menor cantidad de aristas posibles tal que se cumplan las condiciones, es lo mismo que decir que hay que eliminar de $G$ la mayor cantidad de aristas posibles tal que las que se queden cumplan las condiciones.

Debido a que este problema tambien consiste en encontrar $k$ subrafos donde $0 \le k \le minDegree(G)$ la explicación se hará en base a un valor de $k$ fijo.

Esta solución consiste en modelar el grafo $G$ como un problema de flujo de la siguiente manera:

- Se dirige el grafo $G$ de manera tal que: $\forall <u,v> \in E$ si $u \in U$ y $v \in V$ entonces se pone en sentido de $u$ -> $v$
- Se crea un nodo artificial, el cual será la fuente $s$, y este se conecta a todos los vértices de $U$ de forma tal que $\forall u \in U$
$\exist s :$ $s$ -> $u$ $\in E$
- Se crea otro nodo artificial el cual será el receptor $t$, y a este se le conectan todos los vértices de $V$ de forma tal que $\forall v \in V$
$\exist t :$ $v$ -> $t$ $\in E$

```python
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
```

Luego:

- $\forall u \in U : outDegree(u) = k$, no será necesario eliminarle aristas ya que tienen el mínimo posible.

- $\forall u \in U : outDegree(u) > k$, la cantidad a eliminar será la diferencia entre $outDegree(u)$ y $k$, es decir $outDegree(u) - k$

- $\forall v \in V : inDegree(v) = k$, no será necesario eliminarle aristas ya que tienen el mínimo posible.

- $\forall v \in V : inDegree(v) > k$, la cantidad a eliminar será la diferencia entre $inDegree(v)$ y $k$, es decir $inDegree(v) - k$

- $\forall <u, v> \in E : u \in U$ y $v \in V$, es decir las aristas de $G$ sin contar las añadidas por $s$ y $t$. Estas aristas pueden eliminarse una sola vez.

De esta manera queda modelado el grafo: 

- $\forall <s, u> : u \in U$ su capacidad será $outDegree(u) - k$

- $\forall <v, t> : v \in V$ su capacidad será $inDegree(v) - k$

- $\forall <u, v> \in E : u \in U$ y $v \in V$, su capacidad será de 1.

```python
def _create_flow(in_degree: dict, out_degree: dict, min_degree: int, target: int, U: list[int], V: list[int]):
    edges_capacity = {}
    
    for i in U:
        edges_capacity[0, i] = len(out_degree[i]) - min_degree
        edges_capacity[i, 0] = len(out_degree[i]) - min_degree
        for j in out_degree[i]:
            edges_capacity[i, j] = 1
            edges_capacity[j, i] = 1
    for i in V:
        edges_capacity[i, target] = len(in_degree[i]) - min_degree
        edges_capacity[target, i] = len(in_degree[i]) - min_degree
        
    return edges_capacity
```

Después de construir esto solo resta ejecutar el algoritmo de flujo máximo para poder eliminar la mayor cantidad de aristas posibles.

```python
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
```

El costo de este algoritmo es $O(V* \sqrt E)$, por tanto el costo de la solución al tener que ejecutar este algoritmo $k$ veces es:
$O(k*V* \sqrt E)$.

## Generador y Tester

Se crearon 2 archivos .txt donde uno contiene los casos de prueba y el otro las soluciones de estos dadas por el algoritmo de fuerza bruta visto anteriormente. Tanto el generador como el tester son extensibles para los dos ejercicios implementados, basta con cambiar los algoritmos y los nombres de los .txt (o crear otro par nuevo) para que sigan funcionando.

### Generador

```python
def generator():
    U, V = _bipartition_generator()
    adj_list = _edges_generator(U, V)
    return U, V, adj_list
```

Este algoritmo consiste en primeramente generar ambas biparticiones $U$ y $V$, luego se generan aristas entre los vértices de $U$ y $V$, esto es la lista de adyacencia. Luego de tener las biparticiones y la lista de adyacencia ya es un caso válido que cumple las restricciones. Ahora se verá como es que se generan las biparticiones y las aristas.

```python
def _bipartition_generator():
    v = rd.randint(8, 10)
    U, V = [], []
    for i in range(1, v, 1):
        x = rd.randint(0, 1)
        U.append(i) if x == 1 else V.append(i)
    return U, V
```
Primeramente, los vertices fueron definidos como enteros, por tanto una bipartición es una lista de enteros (justo como se vió en el ejemplo de solución).

Luego se genera de forma aleatoria un número, el cuál se refiere a la cantidad de vértices que tendrá el grafo; a continuación se generan enteros (vértices) y cada uno de estos se asignan aleatoriamente a $U$ o $V$ hasta llegar al tope de vértices de forma tal que cada uno pertenezca a solo una bipartición ya que cada entero es generado una única vez.

```python
def _edges_generator(U: list[int], V: list[int]):
    adj_list = {}
    for i in U: 
        adj_list[i] = rd.sample(V, rd.randint(0, len(V)))
        for j in adj_list[i]:
            if(j not in adj_list):
                adj_list[j] = []
            adj_list[j].append(i)
    return adj_list
```
La lista de adyacencia fue implementada en forma de diccionario donde la llave es un vértice $v$ y el valor es una lista de vértices a los cuales $v$ es adyacente.

Para cada vértice $u \in U$ se selecciona aleatoriamente una cantidad aleatoria de vértices $v \in V$ y luego se añaden las aristas correspondientes con esa selección, garantizando por esta forma de generar aristas que nunca serán seleccionados 2 vértices que pertenezcan a una misma bipartición.

Luego, cada caso creado es guardado en tests.txt y son resueltos por el algoritmo de fuerza bruta y guardados en solutions.txt.

NOTA:

Como la solución de cada caso puede no ser única, el algoritmo de fuerza bruta se implementó de forma tal que devolviera todas las soluciones posibles, para que luego nuestro otro algoritmo (que sí devuelve solo una solución) pueda buscar en el conjunto de soluciones posibles para verificar la correctitud del algoritmo.

### Tester

Este módulo simplemente abre tests.txt y cada uno de los casos generados se le pasa a nuestro otro algoritmo y luego se verifica que la solución que este de, pertenezca al conjunto de soluciones que se encuentra en solutions.txt

```python
def tester():
    test, sol = load_txt()
    for i in range(len(test)):
        res = ALGORITHM(test[i])
        flag = False
        for j in range(len(res)):
            if res[j] not in sol[i][j]:
                print(f'Case {i}: Wrong')
                flag = True
        if(not flag):
            print(f'Case {i}: ok')
```