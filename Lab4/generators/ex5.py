def down(N):
    num = N
    while num >= 0:
        yield num
        num -= 1

n = int(input("Enter n: "))
print(*down(n))
