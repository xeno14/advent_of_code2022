import numpy as np

class Rope:

    def __init__(self):
        self.head = np.array([0, 0], dtype=int)
        self.tail = np.array([0, 0], dtype=int)
    
    def move(self, delta: np.array) -> None:
        self.head += delta
        d = self.head - self.tail
        d2 = d[0]**2 + d[1]**2
        if d2 > 2:
            self.tail = self.head - delta

DELTAS = {
    'R': [1, 0],
    'L': [-1, 0],
    'D': [0, -1],
    'U': [0, 1],
}


class RopeN:

    def __init__(self, n: int):
        self.knots = [np.array([0, 0], dtype=int) for _ in range(n)]

    def move(self, delta: np.array) -> None:
        self.knots[0] += delta
        for head, tail in zip(self.knots[:-1], self.knots[1:]):
            d = head - tail
            d2 = d[0]**2 + d[1]**2
            if d2 == 4 or d2 == 8:
                # T.H
                #
                # or
                # 
                # ..H
                # ...
                # T..
                tail[:] += (d // 2)
            elif d2 == 5:
                # ..H
                # T..
                d[0] = d[0] / np.abs(d[0])
                d[1] = d[1] / np.abs(d[1])
                tail += d
            # Otherwise, head and tail are adjacent.

    @property
    def tail(self):
        return self.knots[-1]



def part1(s: str)-> int:
    tail_pos = set()
    rope = Rope()
    for line in s.strip().split('\n'):
        # print(f'=== {line} ===')
        d, n = line.split()
        delta = DELTAS[d]
        n = int(n)
        for _ in range(n):
            rope.move(delta)
            tail_pos.add(tuple(rope.tail))
            # print(rope.head, rope.tail)
    # print(tail_pos)
    return len(tail_pos)


def part2(s: str)-> int:
    tail_pos = set()
    rope = RopeN(10)
    for line in s.strip().split('\n'):
        # print(f'=== {line} ===')
        d, n = line.split()
        delta = DELTAS[d]
        n = int(n)
        for _ in range(n):
            rope.move(delta)
            # tail_pos.add(tuple(rope.tail))
            # print(rope.knots)
            tail_pos.add(tuple(rope.tail))
    # print(tail_pos)
    return len(tail_pos)

EXAMPLE="""
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".strip()

EXAMPLE2="""
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".strip()

assert part1(EXAMPLE) == 13
# print(part2(EXAMPLE))
assert part2(EXAMPLE2) == 36

with open('inputs/day9.txt') as f:
    s = f.read()
print('part1', part1(s))
print('part2', part2(s))


