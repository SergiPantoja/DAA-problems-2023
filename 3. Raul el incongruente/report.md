# Diseño y Análisis de Algoritmos
## Kevin Talavera Díaz - C411
## Sergio Pérez Pantoja - C411

<br>

## Raul el incongruente.

<br>

Raul últimamente quiere impresionar a su novia Daniela, para esto va usar sus habilidades matemáticas, ya que Daniela tiene varias amigos en la facultad y puede apreciar las peripecias de Raul. Raul le pedirá a cada uno de los n amigos matemáticos de Daniela que le diga 2 numeros $a_i$, $b_i$, el segundo mayor o igual que el primero.

Ahora Raul va a efectuar su acto de alta pericia Matemática sin la ayuda siquiera de calculadora, Raul dirá un número entero $x$, tal que para todos los pares dichos por los amigos de Daniela, $x$ no será congruente $a_i$ módulo $b_i$.

<br>

## Nociones de congruencia:

<br>

### Teorema de congruencia lineal:

<br>

Si a y b dos números enteros cualesquiera y n es un número entero positivo, entonces la congruencia: 

$ax \equiv b (mod \text{ } n)$

tiene una solución para x si y solo si b es divisible por el máximo común divisor de a y n (denotado mediante $mcd(a,n)$). Cuando éste es el caso, y $x_0$ es una solución de la ecuación, entonces el conjunto de todas las soluciones está dado por:

$$ x_0 + k \frac {n}{d} | k \in Z$$

En particular, existirán exactamente $d = mcd(a,n)$ soluciones en el conjunto de residuos $0, 1, 2, .., n-1$

<br>

### Sistema de congruencias lineales:

<br>

Sean $m1$ y $m2$ dos naturales primos entre sí. Si cada una de las congruencias lineales:

$a_1x \equiv b_1$ ($mod$ $m_1$)

$a_2x \equiv b_2$ ($mod$ $m_2$)

Tiene solución, entonces existe solución común a ambas congruencias en  $Z$. Si, además, $mcd (a1,m1) = 1$ y $mcd (a2, m2) = 1$, dicha solución es única

<br>

### Teorema chino del resto:

<br>

Supongamos que $n_1, n_2, .., n_k$ son enteros positivos coprimos dos a dos. Entonces, para enteros dados $a_1, a_2, .., a_k$, existe un entero $x$ que resuelve el sistema de congruencias simultáneas

$x \equiv a_1$ ($mod$ $n_1$)

$x \equiv a_2$ ($mod$ $n_2$)

$...$

$x \equiv a_k$ ($mod$ $n_k$)

Más aún, todas las soluciones x de este sistema son congruentes módulo el producto $N$ $= n_1 * n_2 * n_3$.

De manera más general, las congruencias simultáneas pueden ser resueltas si los $n_i$'s son coprimos a pares. Una solución $x$ existe si y solo si:

$a_i \equiv a_j (mod \text{ } mcd(ni, nj)) \text{ } \forall i,j$

Todas las soluciones $x$ son entonces congruentes módulo el $mcm(n_i)$ $\forall i$

<br>

## Ejemplo de solución:

<br>

Sean:

$x \not \equiv a_1$ ($mod$ $n_1$) $\implies$ $x \not = n_1 * k_1 + a_1 $

$x \not \equiv a_2$ ($mod$ $n_2$) $\implies$ $x \not = n_2 * k_2 + a_2 $
 
$x \not \equiv a_3$ ($mod$ $n_3$) $\implies$ $x \not = n_3 * k_3 + a_3 $

Por lo que hay que buscar un valor de $x$ tal q se complan esas ecuaciones.

<br>

## Soluciones

Fueron implementadas 2 soluciones, una con reduccion desde **3-SAT** para demostrar que es **NP** y la otra fue una aproximación mediante una metaheurística de algoritmo genético que funciona mucho más rápido y con una mayor cantidad de ecuaciones en la mayoría de los casos.

## Complejidad:

Este es un problema que pertenece al conjunto conocido como **NP-Completos**.

<br>

### Demostración:

Para demostrar que este problema es **NP-Completo** es necesario demostrar que es **NP** y **NP-Duro**.

<br>

### NP:

Esta parte de la demostración es relativamente sencilla ya que basta con demostrar que la verificación de cualquier candidato a solución puede ser resuelta en tiempo polinomial, lo cual es verdad debido a que: Sea $x$ el valor candidato a solución, se desea verificar si $x$ es incongruente con todas las ecuaciones de congruencia del sistema. Esto se realiza sustituyendo en cada una de las ecuaciones el valor de $x$ y verificando si existe solución para ese valor. Por lo que queda demostrado que el problema es **NP**.

<br>

### NP-Duro:

En esta parte de la demostración se tratará de reducir el bien conocido problema **NP** **3-SAT**.

Fue implementado un algoritmo para detectar cuando una fórmula es satisfacible o no, la cual servirá como tester mas adelante.

```python
def satisfying_assignment(formula):
    {}

    if formula == []:
        return {}

    if [] in formula:
        return None

    soln = {}
    unit_clauses = unit_clause(formula)

    while unit_clauses:
        for literal in unit_clauses:
            formula = help_update(formula, (literal[0], literal[1]))
            
            if [] in formula:
                return None

            soln.setdefault(literal[0], literal[1])
            
            if formula == []:
                return soln

        unit_clauses = unit_clause(formula)

    literal = formula[0][0]

    if literal[1] is True:
        switch_bool = False
    else:
        switch_bool = True

    nu_form = help_update(formula, literal)
    nu_form2 = help_update(formula, (literal[0], switch_bool))

    rec = satisfying_assignment(nu_form)
    if rec is not None:
        soln.update({literal[0]: literal[1]})
        return soln | rec

    rec2 = satisfying_assignment(nu_form2)
    if rec2 is not None:
        soln.update({literal[0]: switch_bool})
        return soln | rec2

    return None
```

En particular, el problema se denomina **3-SAT** cuando las clсusulas tienen longitud tres. Dado que cualquier fórmula en forma normal conjuntiva puede ser escrita con clсusulas de longitud tres, resolver el problema 3SAT es equivalente a resolver el problema **SAT**.

La reducción consiste en asignarle a cada variable de la fórmula lógica un numero primo que la represente, por tanto el primer paso es elegir $p_1, p_2, .., p_n$ donde $p$ es un número primo (para poder aplicar el teorema chino del resto visto anteriormente) y $n$ es el número de variables.

```python
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
```

De esta forma cada cláusula del problema **3-SAT** es codificada como un sistema de congruencias de la forma:

- Sea $V$ el conjunto de variables de la fórmula lógica:

$\forall v \in V \text{ } \exists {\text{ } a \equiv b \text{ } (mod \text{ } p)}$ donde $b \in {1, 0}$ en dependencia si la variable aparece negada o no respectivamente y $p$ es el número primo asociado a $v$.

Luego, por cada cláusula, se agrupan las ecuaciones de congruencia que se correspondan con sus respectivas variables. Por ejemplo:

- Sea $x \lor \lnot y \lor z$ la i-ésima cláusula de la fórmula y $p_1, p_2, p_3$ sus primos asociados respectivamente:

Se obtienen las siguientes ecuaciones:

$a_i \equiv 0$ ($mod$ $p_1$)

$a_i \equiv 1$ ($mod$ $p_2$)

$a_i \equiv 0$ ($mod$ $p_3$)

```python
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
```

Al resolver el sistema de congruencias usando el teorema chino del resto se obtendrá el conjunto de valores de $a$ tales que $a$ sea congruente con los sistemas de congruencias lineales correspondientes a cada cláusula.

*Hasta este momento todo lo explicado han sido transformaciones necesarias para poder reducir una entrada de **3-SAT** a nuestro problema, las cuales son todas polinomiales.*

Por último se crea una ecuación de congruencia con cada uno de los resultados de la siguiente forma:

$x \not \equiv a_1$ ($mod$ $p_1 * p_2 * p_3$)

$x \not \equiv a_2$ ($mod$ $p_1 * p_2 * p_3$)

$...$

$x \not \equiv a_n$ ($mod$ $p_1 * p_2 * p_3$)

```python
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
```

Este sistema coincide con nuestro problema inicial de incongruencias simultáneas, luego, si se logra encontrar un valor de $x$ tal que $x$ sea incongruente a todos en el sistema, la fórmula lógica de es satisfacible, en caso contrario, no lo es, debido a esto la transformación de la salida de nuestro problema a la salida de **3-SAT** es también polinomial, por lo que queda demostrado que nuestro problema es tan o más difícil que **3-SAT** por lo que nuestro problema es **NP-Duro**.

Como ya se demostró que este problema es **NP** y **NP-Duro**, queda demostrado que el problema de Incongruencias simultáneas es **NP-Completo**.


## Generador y Tester

Fue creada una carpeta la en la cual se generan 2 archivos .npy, uno contiene los casos de prueba q consisten en formulas lógicas, y el otro contiene los resultados, los cuales consisten en decir si es satisfacible o no cada formula (método satisfying mencionado enteriormente).

### Generador

Consiste en generar una cantidad de variables y asignarle sus valores (si la variable esta negada es un 1, en caso contrario es 0).

```python
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
```

Como se estan creando entradas de **3-SAT** cada cláusula tendrá exactamente 3 variables.

```python
for i in range(clauses):
        c = list(rd.sample(var, 3))
        formula.append(c)
    return formula
```

### Tester

Este sencillamente carga los casos de prueba creados por el generador, llama al algoritmo implementado y luego verifica si la solución es válida.

```python
def tester():
    t = np.load('TestCases/test.npy', allow_pickle=True)
    s = np.load('TestCases/solutions.npy', allow_pickle=True)
    
    for i in range(len(t)):
        res = an2(t[i])
        if(res == s[i]):
            print('OK')
        else:
            break```
```

...
### Heurística

Para resolver nuestro problema inicial de una manera relativamente eficiente ya que demostramos que es NP, creamos un algoritmo genético.

Los individuos de la población son números enteros, y la población inicial es creada de manera aleatoria con distribución uniforme discreta.

```python
def _generate_initial_pop(size):
    pop = []
    for i in range(size):
        pop.append(np.random.randint(0, 1000000))
    return pop
```

En la función objetivo queremos minimizar el número de congruencias que son satisfechas por $x$. Si en algún momento encontramos un valor de $x$ tal que no satsifaga ninguna congruencia, tenemos una solución válida y terminamos el algoritmo.

```python
def _objective_f(x, congruences):
    num_satisfied = 0
    for i in congruences:
        if check_congruence(x, i[0], i[1]):
            num_satisfied += 1
    return num_satisfied
```

En cada generación, primero calculamos la puntuación o el score de los individuos de la población actual y procedemos al proceso de seleccion de los "padres", al cruce y la mutación.

```python
def _evaluate_pop(population, congruences):
    scores = []
    for i in population:
        #restamos xq queremos minimizar la funcion obj
        score = len(congruences) - _objective_f(i, congruences)
        scores.append(score)
    return scores

def _selection(population, scores):
    #Aqui seleccionamos los padres, los individuos con alto
    #puntaje tendran mas posibilidades de ser seleccionados
    total_fitness = sum(scores)
    prob = [score / total_fitness for score in scores]
    cum_prob = [sum(prob[:i+1]) for i in range(len(prob))]
    r = random.random()
    for i, c_prob in enumerate(cum_prob):
        if r <= c_prob:
            return population[i]

def _crossover(parent1, parent2):
    if abs(parent1 - parent2) <= 2:
        return np.random.randint(1000000)
    child = random.randint(min(parent1, parent2) + 1, max(parent1, parent2) - 1)
    return child

def _mutation(i, mutation_rate):
    r = random.random()
    return np.random.randint(1000000) if (r <= mutation_rate) else i
```

Luego para actualizar la población usada en la siguiente generacion, usamos los padres seleccionados pues tienen alta probabilidad de tener puntaje alto y añadimos los hijos creados con el cruce de estos, o si ocurre una mutación un nuevo individuo producto de la mutación de un hijo.

```python
def genetic_algorithm(generations, pop_size, congruences, mutation_rate):
    pop = _generate_initial_pop(pop_size)
    for gen in range(generations):
        scores = _evaluate_pop(pop, congruences)
        # check if an individual is a valid solution
        for i in range(len(scores)):
            if scores[i] == len(congruences):
                print("Solution found: ", pop[i])
                return pop[i]
        new_pop = []
        while len(new_pop) < pop_size:
            parent1 = _selection(pop, scores)
            parent2 = _selection(pop, scores)
            # keep parents in the population
            new_pop.extend([parent1, parent2])
            # add new children
            child1 = _crossover(parent1, parent2)
            child2 = _crossover(parent1, parent2)
            child1 = _mutation(child1, mutation_rate)
            child2 = _mutation(child1, mutation_rate)
            new_pop.extend([child1, child2])
        while len(new_pop) > pop_size:
            new_pop.pop()
        pop = new_pop
    return -1   #en el caso que ocurran todas las generaciones y no se haya encontrado una solución.
```
