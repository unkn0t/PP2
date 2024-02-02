def spy_game(nums):
    pat = [0, 0, 7]
    pos = 0

    for num in nums:
        if pos >= len(pat):
            break
        if num == pat[pos]:
            pos += 1

    return pos == len(pat)

print(spy_game([1,2,4,0,0,7,5]))
print(spy_game([1,0,2,4,0,5,7]))
print(spy_game([1,7,2,0,4,5,0]))
