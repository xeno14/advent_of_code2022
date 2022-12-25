import collections

EXAMPLE_SMALL="""
.....
..##.
..#..
.....
..##.
.....
""".strip()

EXAMPLE="""
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............
""".strip()


def parse(s: str):
    elves = set()
    lines = s.split('\n')
    rows = len(lines)
    for i, line in enumerate(lines):
        for j in range(len(line)):
            if line[j] == '#':
                elves.add((j, i))
        cols = len(line)
    return elves, cols, rows


def look(elf, dx, dy):
    if dx != 0:
        return [
            (elf[0]+dx, elf[1]-1),
            (elf[0]+dx, elf[1]),
            (elf[0]+dx, elf[1]+1),
        ]
    else:
        return [
            (elf[0]-1, elf[1]+dy),
            (elf[0], elf[1]+dy),
            (elf[0]+1, elf[1]+dy),
        ]

DELTAS = (
            (0, -1),  # North
            (0, 1),  # South
            (-1, 0), # West
            (1, 0),  # East
)

def do_round(elves, nx, ny, round):
    half_round = collections.defaultdict(list)

    for e in elves:
        # Skip if there is no adjacent elf.
        if all((e[0]+dx, e[1]+dy) not in elves for dx, dy in (
            (1,0),
            (1,1),
            (0,1),
            (-1,1),
            (-1,0),
            (-1,-1),
            (0,-1),
            (1,-1),
        )):
            half_round[e].append(e)
            continue

        for i in range(len(DELTAS)):
            dx, dy = DELTAS[(i+round) % len(DELTAS)]

            ee = (e[0]+dx, e[1]+dy)
            # if ee[0] < 0 or ee[0] >= nx or ee[1] < 0 or ee[1] >= ny:
            #     continue
            looking = look(e, dx, dy)
            if any(x in elves for x in looking):
                continue
            half_round[ee].append(e)
            break
        else:
            half_round[e].append(e)
    
    next_elves = set()
    for new_elve, prevs in half_round.items():
        if len(prevs) == 1:
            next_elves.add(new_elve)
        else:
            for e in prevs:
                next_elves.add(e)
    return next_elves


def do_print(elves, nx, ny):
    import numpy as np
    grid = np.zeros((nx, ny), dtype=int)
    for e in elves:
        grid[e] = 1
    # grid = grid.T
    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            print('#' if grid[x, y] else '.', end='')
        print()


def part1(s: str) -> int:
    elves, nx, ny = parse(s)
    # do_print(elves, nx, ny)

    for i in range(10):
        # print()
        # print(f'===== Round {i+1} =====')
        elves = do_round(elves, nx, ny, i)
        # do_print(elves, nx, ny)
    
    xmin=1<<30
    xmax=0
    ymin=1<<30
    ymax=0
    for x, y in elves:
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)

    return (xmax-xmin+1) * (ymax-ymin+1) - len(elves)


def part2(s: str) -> int:
    elves, nx, ny = parse(s)
    # do_print(elves, nx, ny)

    round = 0
    while True:
        prev_elves = elves.copy()
        elves = do_round(elves, nx, ny, round)

        if elves == prev_elves:
            return round+1

        round += 1


assert part1(EXAMPLE) == 110
assert part2(EXAMPLE) == 20

with open('inputs/day23.txt') as f:
    s = f.read()

print('part1', part1(s))
print('part2', part2(s))
