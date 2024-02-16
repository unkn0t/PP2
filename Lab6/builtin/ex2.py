def upper_and_lower(data: str):
    upper = len(list(filter(str.isupper, data)))
    lower = len(list(filter(str.islower, data)))
    return (upper, lower)

data = input("Enter str: ")
upper, lower = upper_and_lower(data)
print(f"Upper: {upper}, Lower: {lower}")
