import os

path = input("Enter path: ")

if os.path.exists(path):
    print("Exist")

    print("Readable:", os.access(path, os.R_OK))
    print("Writeable:", os.access(path, os.W_OK))
    print("Executable:", os.access(path, os.X_OK))
else:
    print("Not exist")
