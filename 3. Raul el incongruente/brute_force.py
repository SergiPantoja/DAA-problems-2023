
def simultaneous_incongruence(nums):
    flag = True
    for i in range(10000000000):
        for j in nums:
            if((i - j[0]) % j[1] == 0):
                flag = True
                break
            else:
                flag = False
        if(not flag):
            return i
    return 'No hay valor'
        

def main():
    nums = [(1, 2), (2, 3), (3, 4)]
    print(simultaneous_incongruence(nums))
    
main()