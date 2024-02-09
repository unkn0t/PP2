def div34(N):
    num = 1
    while num <= N:
        if num % 3 == 0 or num % 4 == 0:
            yield num
        num += 1

n = int(input("Enter n: "))
print(*div34(n))
