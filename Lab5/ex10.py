import re

def camel_to_snake(s: str):
    words = re.findall("[A-Z][^A-Z]*", s)
    return '_'.join(w.lower() for w in words)

s = input("Enter s: ")
print(camel_to_snake(s))
