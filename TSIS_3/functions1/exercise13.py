import random

name = input("Hello! What is your name?\n")

ans = random.randint(1, 20);
print(f"Well, {name}, I am thinking of a number between 1 and 20.")

guess = int(input("Take a guess.\n"))
attempts = 1

while guess != ans:
    if guess < ans:
        print("Your guess is too low.")
    else:
        print("Your guess is too high.")
    
    guess = int(input("Take a guess.\n"))
    attempts += 1
else:
    print(f"Good job, {name}! You guessed my number in {attempts} guesses!")
