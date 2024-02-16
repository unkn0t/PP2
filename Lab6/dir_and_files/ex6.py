letter = ord('A')

while letter <= ord('Z'):
    open(f"{chr(letter)}.txt", 'a').close()
    letter += 1
