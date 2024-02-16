import time
import math

num = float(input())
ms = float(input())

time.sleep(ms / 1000)
res = math.sqrt(num)
print(f"Square root of {num} after {ms} miliseconds is {res}")

