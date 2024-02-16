import os

path = input("Enter path: ")
if os.path.exists(path):
    print("Dirname:", os.path.dirname(path))
    print("Filename:", os.path.basename(path))
