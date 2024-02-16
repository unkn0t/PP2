def num_of_lines(file):
    return len(file.readlines())

path = input("Enter filepath: ")
file = open(path)
print("Lines:", num_of_lines(file))
file.close()
