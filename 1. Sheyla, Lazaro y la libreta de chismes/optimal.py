# Solucion optima
# - Fijamos una permutacion de los 8 tipos de chismes
# - Por cada permutacion hacemos busqueda binaria en x donde x es el valor de la
# frecuencia de cada chisme/longitud de los segmentos continuos minima tal que
# se forme una subsecuencia donde las frecuencias sean x o x+1. Para esto
# buscamos el elemento que menos se repite y su frecuencia es r, hacemos busqueda
# binaria en el intervalo [0, r+1].
# - Para cada x, ejecutamos _find para cada forma de tomar x o x+1 de cada
# elemento (2^8) para encontrar si existe una subsecuencia (si existe ya cumple 
# con las restricciones pues tomo los segmentos continuos y cada chisme aparece
# x o x+1 veces). Si existe tomamos la longitud de la mayor y la guardamos. 
# Luego continuamos busqueda binaria hacia la derecha para ver si existe una 
# subsecuencia con mayor longitud (x mas grande). Si no existe, continuamos 
# busqueda binaria hacia la izquierda para ver si existe una subsecuencia con 
# menor longitud (x mas chico). Si no existe, no existe subsecuencia que cumpla 
# con las restricciones y continuamos con la siguiente permutacion (Aunque 
# siempre existe tomando x = 0).
# - Al finalizar la busqueda binaria tenemos la longitud de la subsecuencia mas
# larga para la permutacion actual (o sea con los valores ordenados de acuerdo
# a la permutacion). Nos quedamos con la mayor longitud de todas las permutaciones.


from itertools import permutations


def optimal(A:str) -> int:
    """Optimal solution, find the longest subsecuence that satisfies the
    constraints"""
    #O(8! * 2^8 * n * log(n))
    
    count = _not_all(A) #Si no hay al menos una ocurrencia de cada elemento, la solucion es 8 menos los que no estan
    if(count != -1):
        return count
    
    minimum = _minimum(A)
    # 8! permutaciones de los 8 tipos de chismes
    p = permutations([1, 2, 3, 4, 5, 6, 7, 8])

    S = 0
    for permutation in p:   #O(8!)
        S = max(S, _binary_search(A, 0, minimum + 1, permutation))  #O(log(n)) len(A) // 8

    return S

def _minimum(arr): #O(n)
    """ Retorna la cantidad minima de ocurrencias del elemento que menos aparece"""
    dic = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
    for i in arr:
        dic[i] += 1
    
    return min(dic.values())

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

def _binary_search(A:str, left:int, right:int, permutation:list) -> int:
    """Binary search for the optimal value of x"""
    #O(log(n) * n)

    max_length = 0
    while left < right:
        mid = (left + right) // 2

        length = _variations(A, mid, permutation)   #O(n)

        if length != -1:
            left = mid + 1
            max_length = max(max_length, length)
        else:
            right = mid
    
    return max_length


total = 0

def _variations(A, mid, permutation):
    global total
    n = [mid, mid + 1]
    m = [-1 for i in range(8)]
    max = [-1]
    _variationsWR(n,m,0, A, permutation, max)
    return max[0]
    
def _variationsWR(n, m, pos, A, permutation, max):
    """por cada forma de poner los elementos de n en m ejecuta el find"""
    #O(2^8)
    global total
    if(pos == len(m)):
        maxAct = _find(A, m, permutation)
        if(maxAct > max[0]):
            max[0] = maxAct
        total +=1
        if(total == 2**8):
            total=0
            return
    else:
        for i in range(len(n)):
            m[pos] = n[i]
            _variationsWR(n, m, pos + 1, A, permutation, max)
    
def _find(A:str, m:list, permutation:list) -> int:
    '''para cada elemento de m ver si se puede tomar esa cantidad de elementos en A dado la permutacion actual'''
    # O(n)
    curr = 0
    count = 0
    totl = 0
    for i in range(len(A)):
        if(int(A[i]) == permutation[curr]):
            count +=1
            if(count == m[curr]):
                curr += 1
                totl += count
                if(curr == len(permutation) and count == m[curr-1]):
                    return totl
                count = 0
    if(curr != len(permutation)):
        return -1
    return totl