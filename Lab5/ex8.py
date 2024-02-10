import re

def at_upper(s: str):
    return re.findall("[A-Z][^A-Z]*", s)

s = input("Enter s: ")
print(at_upper(s))
