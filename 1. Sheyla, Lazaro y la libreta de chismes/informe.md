# Diseño y Análisis de Algoritmos
## Sergio Pérez Pantoja - C311
## Kevin Talavera Díaz - C311

<br>

## Sheyla, Lázaro y la libreta de chismes.

A Sheyla le gusta el chisme. De hecho, le gusta a tal punto que tiene una libreta con todos los secretos de su aula de los que se ha ido enterando con el paso de los años. Los chismes da la libreta están ordenados por tiempo de descubrimiento y separados en 8 categorías distintas (vergonzoso, para enorgullecerse, amoroso, etc).

Por otro lado, las vueltas de la vida han llevado a Lázaro a volverse presidente del aula y, para mantener su poder, ha decidido que resultaría conveniente conocer secretos de sus compañeros (quéin sabe, pueden resultar útiles) y le ha pedido ayuda a Sheyla. Sin embargo, Lázaro es un poco raro y también ha decidido que no necesita todos los secretos de la libreta, sino un subconjunto de estos que cumpla con las siguientes condiciones:

Sea $A$ una cadena con enteros entre 1 y 8. Cada índice representa un chisme de la libreta (en el mismo orden en que aparece) y cada valor representa el tipo de chisme asociado a este. Además, la cadena $S$ representa el subconjunto que Lázaro quiere conocer.

- Para cada par de tipos de chismes $t_1$, $t_2$ distintos, la cantidad de chismes de tipo $t_1$ en $S$ puede diferir de la cantidad de chismes de tipo $t_2$ en no más de 1 elemento.
- Si un chisme de tipo $t$ aparece en $S$, todos los chismes de tipo $t$ de $S$ deben formar un segmento continuo. Estos chismes no son necesariamente continuos en la cadena $A$.

Para ayudar a Lázaro y Sheyla, reciba la cadena $A$ representando a la libreta, y calcule el tamaño de la mayor cadena $S$ posible.

<br>

## Ejemplo de solución del problema

Se tomarán números del 1 al 3 para facilitar la comprensión, pero todo el código esta como la orden lo plantea, del 1 al 8.

Sea la lista de entrada:

```python
A = [1, 1, 2, 3, 2, 3, 1, 3]
```

Tenemos 4 condiciones que cumplir:

* Si ya se tiene un numero en la lista de resultado, todos sus iguales tienen que venir consecutivos, y sus respectivos índices en la lista original tienen que estar en orden creciente

    ```python
    [1, 2, 3]
    [1, 1, 2, 3, 3, 3]
    [1, 1, 2, 2, 3, 3]
    ```

* La subsecuencia resultante tiene que tener la mayor cardinalidad posible:

    ```python
    [1, 1, 2, 3, 3, 3]
    [1, 1, 2, 2, 3, 3]
    ```

* Si uno de los números del 1 al 8 no aparece en la solución, esto cuenta como cardinalidad 0 en el resultado.

* Para cada subconjunto en la lista de resultado la diferencia entre sus cardinalidades tiene que ser a lo sumo 1:

    ```python
    [1, 1, 2, 2, 3, 3]
    ```

Si cumplen estas 3 condiciones el problema está resuelto, en el caso de este ejemplo la solución es la última lista mostrada.

<br>

## Ideas abordadas

### Combinatioria:
La primera idea que se pensó fue resolver el problema por combinatoria, se  generan todas las posibles combinaciones que puede tener la lista de entrada y luego se verifica cuál/es cumplen las condiciones antes mencionadas. Este algoritmo fue implementado como tester y será explicado en detalle más adelante.

### Subsecuencia máxima creciente:
Luego se el problema fue modelado de forma tal que se resolviera usando el algoritmo de máxima subsecuencia creciente. La idea fue:

Tomar la lista de entrada del problema (A partir de ahora esta lista se denotará como $L$) junto con sus índices:

```python
A = [1, 1, 3, 2, 3, 2, 1, 2]
I = [0, 1, 2, 3, 4, 5, 6, 7]
```

Luego se agrupan los elementos de la lista en orden de aparición y se guardan en una lista la actualización de los índices que dio como resultado construir esta permutación

Permutación (A partir de ahora esta lista se denotará como $P$) y los índices actualizados $I$:

```python
[1, 1, 1, 3, 3, 2, 2, 2]
[0, 1, 6, 2, 4, 3, 5, 7]
```

Al obtener esta lista de ¨índices¨ se garantiza que $\forall x,y \in I$ si $x < y$ significa que $x$ aparece antes que $y$ en $L$.

Por tanto si se obtiene la máxima subsecuencia creciente de $I$:

```python
[0, 1, 2, 3, 5, 7]
```

se garantiza que si $x > y$, $x$ no va a aparecer antes que $y$ en la solución, la cual es una de las condiciones del ejercicio, además, como $I$ se obtuvo a partir de los cambios que llevaron de $L$ a $P$ y en este cada subconjunto de números está garantizado que $\forall x,y \in P : x = y$ , $x$ es consecutivo con $y$, en $I$ ocurre lo mismo y por ende una solución usando este algoritmo también cumpliría esta propiedad. Hasta este punto el problema podría ser resuelto en $O(n log n)$, pero no se encontró manera de mantener un tiempo similar a este añadiendo el cumplimiento de la restricción de la diferencia de las cardinalidades ya que esto implicaba tener que usar backtrack, por lo que esta solución fue descartada.

### Óptimo:

Idea general de la solución:

1. Se toman todos los posibles ordenes en los que pueden aparecer cada conjunto en la solución (todas las permutaciones de [ 1 … 8]).

2. Para cada una se busca cual es el tamaño de la subsecuencia máxima que se pudo encontrar.

3. De los máximos de tamaño de cada una de las permutaciones, la solución es el mayor entre ellos.

Demostración:

- Sea A la lista de entrada tal que $\forall i \in A: 1 \le i \le 8$.

-  Sea $S$ la subsecuencia máxima que cumple las restricciones (La solución óptima del problema).

- Sea $P$ el conjunto de todas las permutaciones de [1, 2, 3, 4, 5, 6, 7, 8] donde cada $p \in P$ representa el orden en que se toman los segmentos continuos de números iguales de la solución.

- Tomamos la primera aparición de cada elemento diferente de $S$ y supongamos que la lista formada $p' \notin P$.

- Luego, como $S$ es subsecuencia de $A$ tiene todos los números del 1 al 8 (excepto en el caso donde uno o más números no aparezcan en $A$) y al tomar cada uno en el orden en que aparecen esta lista es una permutación de [1, 2, 3, 4, 5, 6, 7, 8] que por definición $=> p' \in P$ por tanto tenemos una contradicción por lo que tomando la primera aparición de cada elemento diferente de $S$ obtenemos una permutación que pertenece a $P$.

- En el caso que no aparezca uno o más números en $A$ entonces $S$ es una secuencia donde aparece cada elemento diferente de $A$ solo una vez. [1]

- Como el algoritmo encuentra la secuencia más larga con los segmentos contiguos ordenados según cada permutación para todas las permutaciones de $P$, va a encontrar a $S$.

El algoritmo se verá en el apartado de ALGORITMOS.

<br>

## Generador y Tester:

Se crearon 2 archivos .txt donde uno contiene los casos de prueba y el otro las soluciones de estos dadas por el algoritmo combinatorio que se verá más adelante.

### Generador

```python
def Generator():
    res = []
    for i in range(100):
        tam = rd.randint(0,20)
        list = []
        for j in range(tam):
            num = rd.randint(1, 8)
            list.append(num)
        res.append(list)
    return res
```

Este algoritmo genera todo tipo de casos de prueba validos ya que las listas de entrada son de tamaño arbitrario, en este caso se toma un numero aleatorio entre 0 y 20 debido a que el algoritmo combinatorio demora mucho en resolver el problema para tamaños mayores. La otra condición es que se genere un número aleatorio del 1 al 8 para cada posición de la lista, y estos pueden repetirse cualquier cantidad de veces y en cualquier orden, el método lo resuelve generando números aleatorios para cada posición de la lista.

### Tester

```python
def Tester():
    test, sol = LoadTxt()
    for i in range(len(test)):
        res = optimal(list(test[i][0:len(test[i])-1]))
        if(res == int(sol[i])):
            print(f'Case {i}: OK')
        else:
            print(f'Case {i}: Wrong')
```

Se guardan en una lista los casos prueba con sus respectivas soluciones y luego al algoritmo optimo se le pasan cada uno de los casos y se verifica si su resultado es 
correcto

<br>

## Algoritmos

<br>

### Naive (Fuerza bruta)

El primer algoritmo pensado fue el más intuitivo, el cual es una solución muy ineficiente, pero es la más sencilla de demostrar su correctitud y complejidad. Esta es la solución por combinatoria, la cual consiste en generar todos los posibles resultados y devolver el/los que cumplan los requisitos anteriormente mencionados.


```python
def Combinations(arr):
    comb = []
    for i in range(len(arr)):
        comb.append(combinations(arr, i+1))
    return comb
```

En este fragmento se utiliza el módulo itertools.combinatios, el cual hace uso del método combinations, este recibe una lista y un valor $k$ (tamaño de la combinación) Como el objetivo es generar todas las posibles combinaciones de la lista de entrada basta con generar todas las combinaciones variando el número de $k$ entre $1 \le k \le n$ donde $n$ es el tamaño de la lista, es decir, estamos generando el conjunto potencia de la lista de entrada. Las combinaciones generadas se guardan en una variable y se devuelven para luego analizar el cumplimiento de las restricciones. Esto es $O(2^n)$ que es la cantidad de elementos en el conjunto potencia de tamaño $n$.

Luego de obtener todas las combinaciones, se verifica cual o cuales cumplen las condiciones:

- Condición 1:

```python
def Sets(arr):
    dic = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for i in arr:
        dic[i] += 1
    for i in range(len(arr)-1):
        dic[arr[i]] -= 1
        if(arr[i] != arr[i+1] and dic[arr[i]] > 0):
            return False
    return True
```

Este método primeramente cuenta cuantas veces se repite cada elemento de la lista y lo guarda en un diccionario, eso es $O(n)$. Luego como se quiere saber si los números que son iguales en la solución aparecen de forma consecutiva, lo que se hace es recorrer la lista nuevamente y se verifica si la cantidad de elementos consecutivos coincide con el valor guardado en el diccionario, en caso de que el algoritmo recorra la lista completa significa que no encontró problemas y la solución es válida, en caso contrario si la cantidad de elementos consecutivos es menor que la cantidad de ocurrencias totales significa que existe al menos un conjunto de números entre los consecutivos verificados y los que faltaron, por lo que esto es invalido. La complejidad temporal de este método es: $O(n + n) = O(n)$

- Condición 3:

```python
def NotAll(arr):
    count = 0
    dic = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for i in arr:
        dic[i] += 1
    for i in dic:
        if(dic[i] > 0):
            count += 1
    if(count == 8):
        return -1
    return count
```

Este método verifica si cada número del 1 al 8 aparece al menos una vez en la lista de entrada, ya que en caso de no ser así, en la lista de resultado solo podrá existir a lo sumo 1 de cada número que este en la entrada y el resultado seria 8 − 𝑥 donde 𝑥 es la cantidad de números del 1 al 8 que no aparecen. Este método es $O(n + 8) = O(n)$

- Condición 4:

```python
def Difference(arr):
    dic = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for i in arr:
        dic[i] += 1
        
    dif = [dic[i] for i in dic]
    
    if(max(dif) - min(dif) > 1):
        return False
    return True
```

Este método, al igual que el anterior cuenta las ocurrencias de cada elemento de la lista y como se quiere verificar si las cardinalidades para todo par de conjunto de elementos difieren en a lo sumo 1, basta con obtener cual es el conjunto que tiene más elementos y cuál es el que menos, si la diferencia es mayor 1 no se cumple la restricción por tanto no es solución, en caso contrario si pertenece. Hacer esta resta funciona debido a que todas las cardinalidades de los conjuntos están acotadas por: $min \le x_i \le max : 1 \le i \le 8$ donde $x_i$ es la cardinalidad asociada al conjunto $i$, así que si la diferencia entre el mínimo y el máximo es menor o igual que 1, también lo será para cualquier elemento entre el máximo y otro mayor que el mínimo y viceversa. La complejidad temporal de este método es $O(n + 8 + n) = O(n)$

- Condición 2:

```python
def Naive(arr):
    count = NotAll(arr)
    if(count != -1):
        return count
    combs = Combinations(arr)
    result = []
    max = 0
    for i in range(len(combs)-1, 0, -1):
        for j in list(combs[i]):
            if(len(j) < max):
                return result
            if(Sets(j) and Difference(j)):
                max = len(j)
                result.append(j)
    return result
```

En el caso mejor: Si no aparece al menos uno de cada número en la entrada, ya que de ser así el resultado es el que se explicó anteriormente sin necesidad de buscar combinaciones u otra verificación es $O(n)$.

Esta condición se resuelve en la ejecución del método principal del algoritmo ya que, si el objetivo es encontrar la subcadena máxima, basta con recorrer la lista de todas las posibles combinaciones, la cual esta ordenada de forma creciente (ver Fig1) comenzando desde la última posición hasta el comienzo, de esta forma la primera cadena que cumpla las otras dos condiciones explicadas anteriormente 
será la de tamaño máximo. (En este caso, esta solución fue la implementada para el tester, por tanto, se le añadió que encontrara todas las cadenas máximas ya que esta puede no ser única y no tener problemas con algoritmos más eficientes que solo dan una óptima). La complejidad del algoritmo en general es la complejidad de este método en un caso que no sea el mejor (el peor ) es: $O(2^n * (n + n)) = O(n * 2^n)$

### Òptimo

Este es el algoritmo más eficiente pensado, su idea general fue la explicada anteriormente, pero ahora será vista en más detalle.

```python
def _not_all(arr): #O(n)
    """si no hay al menos 1 ocurrencia de cada elemento devuelve cuantos hay"""
    count = 0
    dic = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
    for i in arr:
        dic[i] += 1
    for i in dic:
        if(dic[i] > 0):
            count += 1
    if(count == 8):
        return -1
    return count
```
Si en la lista de entrada no existe al menos una ocurrencia de cada elemento, al igual que en la solución por combinatoria el resultado es tomar un elemento por cada uno que aparece, y este es el mejor caso y se resuelve en 𝑂(𝑛).

```python
def _minimum(arr): #O(n)
    """ Retorna la cantidad minima de ocurrencias del elemento que menos aparece"""
    dic = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
    for i in arr:
        dic[i] += 1
    
    return min(dic.values())
```
Sea $x$ la cantidad de veces que se repite el número que menos se repite de la lista de entrada, en el óptimo no puede existir ningún conjunto con cardinalidad mayor a $x + 1$. Esto sirve como cota para mejorar el algoritmo que será explicado más adelante.

Sea $f_i, f_j$ la cantidad de veces que se repite los elementos $i, j$ en $S$, es decir la frecuencia de $i$ o $j$ en $S$. Como tenemos como restricción del problema que $|f_i - f_j| \le 1$ entonces si el mínimo es $x$ no puede existir en la solución un elemento que se repita $x + i$ veces tal que $i \ge 2$. 

- si el número que se repite $x$ veces se pone esa cantidad de veces en la solución, los restantes solo pueden repetirse exclusivamente $(x \land (x + 1))$ $\lor$ $(x \land (x - 1))$ veces