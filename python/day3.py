EXAMPLE = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()


def part1(s: str):
    ans = 0
    for line in s.split('\n'):
        half_size = len(line) // 2
        first, second = line[:half_size], line[half_size:]
        common_set = set(first) & set(second)
        common = common_set.pop()
        if common.islower():
            value = ord(common) - ord('a') + 1
        else:
            value = ord(common) - ord('A') + 27
        ans += value
    return ans


def part2(s: str):
    ans = 0
    lines = s.split('\n')
    for i in range(0, len(lines), 3):
        common_set = set(lines[i]) & set(lines[i+1]) & set(lines[i+2])
        common = common_set.pop()
        if common.islower():
            value = ord(common) - ord('a') + 1
        else:
            value = ord(common) - ord('A') + 27
        ans += value
    return ans



assert part1(EXAMPLE) == 157
assert part2(EXAMPLE) == 70
with open('input/day3.txt') as f:
    s = f.read()

print(part1(s))
print(part2(s))


        




