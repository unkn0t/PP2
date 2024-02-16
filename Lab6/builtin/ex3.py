def is_palindrome(data: str):
    rev = ''.join(reversed(data))
    return rev == data

data = input("Enter str: ")
print(is_palindrome(data))
