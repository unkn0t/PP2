# Exercise 5
from itertools import permutations

def all_permutations(s):
    for perm in permutations(s):
        print(''.join(perm))

s = input("Enter string: ")
all_permutations(s)
