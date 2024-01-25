class Person:
    def __init__(self, fname):
        self.firstname = fname

    def printname(self):
        print(self.firstname)

# Exercise 1
class Student(Person):
    pass

# Exercise 2
x = Student("Mike")
x.printname()
