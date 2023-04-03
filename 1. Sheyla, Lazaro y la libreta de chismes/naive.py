from itertools import combinations

def Combinations(arr):
    comb = []
    for i in range(len(arr)):
        comb.append(combinations(arr, i+1))
    return comb

def Difference(arr):
    dic = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for i in arr:
        dic[i] += 1
        
    dif = [dic[i] for i in dic]
    
    if(max(dif) - min(dif) > 1):
        return False
    return True

def Sets(arr):
    dic = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for i in arr:
        dic[i] += 1
    for i in range(len(arr)-1):
        dic[arr[i]] -= 1
        if(arr[i] != arr[i+1] and dic[arr[i]] > 0):
            return False
    return True

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