def fahrenheit_to_centigrade(F):
    return (5 / 9) * (F - 32)

F = float(input("Enter temperature in [F]: "))
C = fahrenheit_to_centigrade(F)
print(f"Temperature in [C]: {C}")
