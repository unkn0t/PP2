# Exercise 1
class Upper:
    def getString(self):
        self.s = input("Input string: ") 

    def printString(self):
        print(self.s.upper())

# Exercise 2
class Shape:
    def __init__(self, length):
        self.length = length

    def area(self):
        return 0

class Square(Shape):
    def area(self):
        return self.length ** 2

# Exercise 3
class Rectangle(Shape):
    def __init__(self, length, width):
        super().__init__(length)
        self.width = width

    def area(self):
        return self.width * self.length

# Exercise 4
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"{self.x}, {self.y}")

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def dist(self, other):
        if type(other) is Point:
            return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2) 
        else:
            raise Exception("other must be a point")

# Exercise 5
class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(self.balance)

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        print(self.balance)

acc = Account("ABOBA", 10)
acc.deposit(1);
acc.withdraw(5);
acc.withdraw(7);
acc.deposit(10);
acc.withdraw(7);

# Exercise 6
def prime(x):
    if x == 1:
        return False

    for d in range(2, x):
        if x % d == 0:
            return False
    return True
    
nums = [x for x in range(1, 31)]
nums = list(filter(lambda x: prime(x), nums))
print(nums)
