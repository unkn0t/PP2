def squares(N):
    num = 1
    while num <= N:
        yield num * num
        num += 1

n = int(input("Enter N: "))
for sqr in squares(n):
    print(sqr, end=' ')
