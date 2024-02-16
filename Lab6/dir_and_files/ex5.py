lst = [1, 2, 3, 4, 5]

with open("list.txt", "w") as file:
    file.write(str(lst))
    file.write('\n')
    # Or
    for el in lst:
        file.write(f"{el} ")

