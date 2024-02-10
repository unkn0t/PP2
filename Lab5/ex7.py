import re

def snake_to_camel(s: str):
    return ''.join(w.capitalize() for w in re.split('_', s))

s = input("Enter s: ")
print(snake_to_camel(s))
