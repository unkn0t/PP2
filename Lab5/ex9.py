import re

def spacify(s: str):
    words = re.findall("[A-Z][^A-Z]*", s)
    return ' '.join(words)

s = input("Enter s: ")
print(spacify(s))
