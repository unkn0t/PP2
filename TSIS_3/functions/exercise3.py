def solve(numheads, numlegs):
    rabbits = numlegs // 2 - numheads 
    chikens = numheads - rabbits
    return (chikens, rabbits)

print(solve(35, 94))
