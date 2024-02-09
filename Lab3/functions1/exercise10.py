def unique(lst):
    res = []
    for el in lst:
        if res.count(el) == 0:
            res.append(el)
    return res

print(unique([1, 2, 1, 3, 2, 2]))
