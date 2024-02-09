import math

n = int(input("Input number of sides: "))
l = float(input("Input the length of a side: "))

apoth = l / (2 * math.tan(math.radians(180 / n)))
area = n * l * apoth / 2

print("The area of the polygon is: ", area)
