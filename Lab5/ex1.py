import re

s = input("Enter str: ")
match = re.search("ab+", s)
if match == None:
    print("Do not match")
else:
    print(f"Match {match[0]}")
