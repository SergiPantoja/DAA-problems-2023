
def satisfies_constraints(subsecuence:str) -> bool:
    #O(n), where n is the length of the subsecuence

    types = [False for i in range(8)]
    count = [0 for i in range(8)]

    for i in range(len(subsecuence)):
        count[int(subsecuence[i]) - 1] += 1
        if types[int(subsecuence[i]) - 1]:   #if the character has already appeared
            if (subsecuence[i] != subsecuence[i - 1]):   #if the character is not consecutive
                #print("no es consecutivo", subsecuence[i], subsecuence[i - 1], subsecuence)
                return False
        else:
            types[int(subsecuence[i]) - 1] = True

    #tiempo constante O(8*8)   
    for i in range(len(count)):
        for j in range(i+1, len(count)):
            if abs(int(count[i]) - int(count[j])) > 1:
                #print("no cumple la cantidad", i+1, j+1, count)
                return False

    return True


def naive(A:str) -> int:
    """Naive solution, find all posible subsecuences and return the size of 
    the longest that satisfies the constraints"""
    #O(2^n * n)

    subsecuences = (_naive_recursive(A, set(), "")) #O(2^n)
    #print("subsecuences: ", len(subsecuences), subsecuences)

    max = 0
    longest = ""
    #2^n subsecuences de a lo sumo longitud n donde n es la longitud de A
    #O(n) satisfies_constraints
    #O(2^n * n)
    for subsecuence in subsecuences:
        if satisfies_constraints(subsecuence):
            if len(subsecuence) > max:
                max = len(subsecuence)
                longest = subsecuence
    
    print("longest: ", longest)
    return max

def _naive_recursive(A:str, subsecuences:set, secuence:str) -> set:

    #O(2^n), len(A) = n
    #Estamos generando todas las subsecuencias en un str the longitud n, esto
    #es conjunto potencia de n, que es 2^n
    #annadir a un set es O(1) amortizado???

    if len(A) == 0:
        subsecuences.add(secuence)
        #print(secuence)
        return
    
    _naive_recursive(A[1:], subsecuences, secuence + A[0])
    _naive_recursive(A[1:], subsecuences, secuence)

    return subsecuences


def naivito(A:str) -> int:

    s =  _naivito_recursive(A, set(), "", [False for i in range(8)], [0 for i in range(8)])

    max = 0
    longest = ""
    for subsecuence in s:
        if len(subsecuence) > max:
            max = len(subsecuence)
            longest = subsecuence

    print("longest: ", longest)
    return len(longest)

def _naivito_recursive(A:str, s:set, secuence_curr:str, types:[bool], count:[int]) -> str:
    """ lo mismo pero si es una subsecuencia invalida poda """

    if len(A) == 0:
        for i in range(len(count)):
            for j in range(i+1, len(count)):
                if abs(int(count[i]) - int(count[j])) > 1:
                    return
        #if len(secuence_curr) > len(longest):
        #    longest = secuence_curr
        s.add(secuence_curr)
        return

    
    if types[int(A[0]) - 1]:  #if the character has already appeared
        first_appearance = False
        if (A[0] != secuence_curr[-1]):  #if the character is not consecutive
            s.add(secuence_curr)
            return     
    else:
        types[int(A[0]) - 1] = True
        first_appearance = True
    count[int(A[0]) - 1] += 1
    _naivito_recursive(A[1:], s, secuence_curr + A[0], types, count)

    count[int(A[0]) - 1] -= 1
    if first_appearance:
        types[int(A[0]) - 1] = False
        first_appearance = False
    _naivito_recursive(A[1:], s, secuence_curr, types, count)

    return s



if __name__ == "__main__":
    print("longest: ", naive("32277188744365566"))
    print("\n\n")
    print("longest2: ", naivito("32277188744365566"))

    print("longest: ", naive("12233456788232"))
    print("\n\n")
    print("longest2: ", naivito("12233456788232"))

    print("longest: ", naive("135421784671"))
    print("\n\n")
    print("longest2: ", naivito("135421784671"))