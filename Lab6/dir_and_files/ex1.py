import os

path = input("Enter path: ")
all = os.listdir(path)
files = list(filter(lambda x: os.path.isfile(os.path.join(path, x)), all))
dirs = list(filter(lambda x: os.path.isdir(os.path.join(path, x)), all))
print("Dirs and Files:", all)
print("Files:", files)
print("Dirs:", dirs)
