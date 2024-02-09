def even(N):
    num = 1
    while num < N:
        if num % 2 == 0:
            yield num
        num += 1

n = int(input("Enter n: "))
print(*even(n), sep=',')
