def squares(a, b):
    num = a
    while num <= b:
        yield num * num
        num += 1

for x in squares(2, 8):
    print(x)
