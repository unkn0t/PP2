def prime(num):
    if num == 1:
        return False
    for d in range(2, num):
        if num % d == 0:
            return False
    return True

def filter_prime(nums): 
    return [num for num in nums if prime(num)] 

nums = map(int, input("Enter numbers: ").split(' '))
print(filter_prime(nums))
