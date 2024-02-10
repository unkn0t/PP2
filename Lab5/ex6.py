import re

s = input("Enter str: ")
res = re.sub(r"[\s.,]", ":", s)
print(res)
