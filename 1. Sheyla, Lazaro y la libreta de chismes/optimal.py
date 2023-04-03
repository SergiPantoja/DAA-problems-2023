# Solucion optima
# - Fijamos una permutacion de los 8 tipos de chismes
# - Por cada permutacion hacemos busqueda binaria en x donde x es el valor de la
# frecuencia de cada chisme/longitud de los segmentos continuos minima tal que
# se forme una subsecuencia donde las frecuencias sean x o x+1
# - Para cada x, realizamos greedy o dp para encontrar si existe una subsecuencia
# (si existe ya cumple con las restricciones pues tomo los segmentos continuos
# y cada chisme aparece x o x+1 veces). Si existe tomamos la longitud de la mayor
# (greedy siempre me va a dar la mayor) y la guardamos. Luego continuamos 
# busqueda binaria hacia la derecha/arriba para ver si existe una subsecuencia
# con mayor longitud (x mas grande). Si no existe, continuamos busqueda binaria
# hacia la izquierda/abajo para ver si existe una subsecuencia con menor longitud
# (x mas chico). Si no existe, no existe subsecuencia que cumpla con las
# restricciones y continuamos con la siguiente permutacion. Siempre existe
# tomando x = 0.
# - Al finalizar la busqueda binaria tenemos la longitud de la subsecuencia mas
# larga para la permutacion actual (o sea con los valores ordenados de acuerdo
# a la permutacion). Nos quedamos con la mayor longitud de todas las permutaciones.


from itertools import permutations


def optimal(A:str) -> int:
    """Optimal solution, find the longest subsecuence that satisfies the
    constraints"""
    #O(8! * n * log(n))
    
    # 8! permutaciones de los 8 tipos de chismes
    p = permutations([1, 2, 3, 4, 5, 6, 7, 8])

    S = 0
    for permutation in p:   #O(8!)
        S = max(S, _binary_search(A, 0, len(A), permutation))  #O(log(n)) len(A) // 8

    return S

def _binary_search(A:str, left:int, right:int, permutation:list) -> int:
    """Binary search for the optimal value of x"""
    #O(log(n) * n)

    max_length = 0
    while left < right:
        mid = (left + right) // 2

        exists, length = _greedy(A, mid, permutation)   #O(n)

        if exists:
            left = mid + 1
            max_length = max(max_length, length)
        else:
            right = mid
    
    return max_length
    


def _greedy(A:str, x:int, permutation:list) -> tuple[bool, int]:
    # O(n)
    
    total_length = 0
    segment_length = 0
    curr = 0
    for i in range(len(A)):
        if int(A[i]) == permutation[curr]:      # Si estoy sobre el valor q toca
            segment_length += 1                 # Sumo 1 a la longitud del segmento correspondiente a ese valor
            if segment_length == x + 1:         # Ya no puedo tomar mas valores de ese tipo
                curr += 1                       # Paso al siguiente tipo de chisme
                if curr == len(permutation):    # Si ya termine de tomar todos los tipos de chismes
                    total_length += segment_length
                    return True, total_length  # Devuelvo la longitud de la subsecuencia
                    break
                total_length += segment_length
                segment_length = 0

        elif int(A[i]) != permutation[curr]:    # Si estoy sobre un valor que no toca
            if segment_length < x:              # Si el segmento no llego a la longitud minima
                continue                        # Sigo buscando mas elementos del mismo tipo
            else:   # x o x+1 elementos del tipo actual
                # Si no es el ultimo tipo de chisme y estoy sobre el siguiente tipo de chisme
                if (curr != len(permutation) - 1) and (int(A[i]) == permutation[curr + 1]):
                    curr += 1                       # Paso al siguiente tipo de chisme, que es en el que estoy
                    total_length += segment_length
                    segment_length = 1
                else:
                    # tenemos >= x elementos del tipo actual.
                    # 1. Estamos sobre un valor que no es el tipo actual ni el siguiente
                    # 2. Estamos sobre el ultimo tipo curr == len(permutation) - 1
                    # En cualquier caso sigo buscando un posible elemento x+1 del tipo actual
                    # o el primer elemento del siguiente tipo
                    continue
        
    if (curr == len(permutation) - 1) and segment_length >= x:
        total_length += segment_length
        return True, total_length
    else:
        return False, 0