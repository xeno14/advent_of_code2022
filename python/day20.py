from collections import *

EXAMPLE="""
1
2
-3
3
-2
0
4
""".strip()


def move_deque(a: deque[int], key: tuple[int, int]):
    n, _ = key
    i = a.index(key)
    a.rotate(-i)
    a.popleft()
    a.rotate(-n)
    a.appendleft(key)


def part1(s: str) -> int:
    keys = [(int(x), i) for i, x in enumerate(s.split('\n'))]
    for key in keys:
        if key[0] == 0:
            key0 = key
            print(f'{key0=}')
    a = deque(keys)
    for key in keys:
        move_deque(a, key)
    a.rotate(-a.index(key0))
    ans = 0
    for i in [1000, 2000, 3000]:
        print(f'a[{i}]={a[i%len(a)]}')
        ans += a[i%len(a)][0]

    return ans


def part2(s: str) -> int:
    DEC_KEY = 811589153

    keys = [(int(x) * DEC_KEY, i) for i, x in enumerate(s.split('\n'))]
    for key in keys:
        if key[0] == 0:
            key0 = key
            print(f'{key0=}')
    a = deque(keys)

    for i in range(10):
        print(f'Round {i}')
        for key in keys:
            move_deque(a, key)
    a.rotate(-a.index(key0))
    ans = 0
    for i in [1000, 2000, 3000]:
        print(f'a[{i}]={a[i%len(a)]}')
        ans += a[i%len(a)][0]

    return ans

assert part1(EXAMPLE) == 3
assert part2(EXAMPLE) == 1623178306

with open('inputs/day20.txt') as f:
    s = f.read()
print('part1', part1(s))
print('part2', part2(s))