import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Provide file to delete")
        return

    path = sys.argv[1]

    if not os.path.exists(path):
        print("File does not exist")
        return 
    if not os.access(path, os.W_OK):
        print("Not enough rights to delete")
        return
    
    os.remove(path)

main()

