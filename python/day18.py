import numpy as np

EXAMPLE="""
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".strip()


FACES = [
    np.array([1, 0, 0]),
    np.array([-1, 0, 0]),
    np.array([0, 1, 0]),
    np.array([0, -1, 0]),
    np.array([0, 0, 1]),
    np.array([0, 0, -1]),
]


def parse(s: str) -> list[tuple[int, int, int]]:
    return [np.array([int(x) for x in line.split(',')], dtype=int) for line in s.split('\n')]


def part1(s: str) -> int:
    # Scale x2.
    cubes = parse(s)
    cubes = [
        p * 2 for p in cubes
    ]
    faces = set()
    for cube in cubes:
        for delta in FACES:
            key = tuple(cube + delta)
            if key in faces:
                faces.remove(key)
            else:
                faces.add(key)
    return len(faces)


def part2(s: str) -> int:
    cubes = np.array(parse(s))
    cubes += 1  # offset
    tcube = cubes.T
    shape = tuple(tcube[i].max()+3 for i in range(3))
    is_cube = np.zeros(shape, dtype=bool)
    for cube in cubes:
        is_cube[tuple(cube)] = True

    ans = 0
    def dfs(pos, visited):
        nonlocal ans

        visited.add(pos)
        for delta in FACES:
            nxt = tuple(delta + pos)
            if any(nxt[i] < 0 or nxt[i] >= is_cube.shape[i] for i in range(3)):
                continue
            if is_cube[nxt]:
                ans += 1
            elif nxt not in visited:
                dfs(nxt, visited)

    dfs((0,0,0), set())
    return ans


assert part1(EXAMPLE) == 64
assert part2(EXAMPLE) == 58
with open('inputs/day18.txt') as f:
    s = f.read()
import sys
print(sys.setrecursionlimit(200000))
print('part1', part1(s))
print('part2', part2(s))
