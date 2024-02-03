def is_palindrom(s):
    for i in range(len(s) // 2):
        if s[i] != s[-i-1]:
            return False
    return True

print(is_palindrom("madam"))
print(is_palindrom("chair"))
print(is_palindrom("cabbac"))
