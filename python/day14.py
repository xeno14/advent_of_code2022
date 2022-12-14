import numpy as np


NOTHING = 0
WALL = 1
SAND = 2


def parse(s: str) -> np.array:
    strokes = []
    for line in s.split('\n'):
        stroke = []
        for points in line.split(' -> '):
            x, y = points.split(',')
            stroke.append((int(x), int(y)))
        strokes.append(stroke)

    grid = np.zeros(shape=(1000, 170), dtype=int)
    for stroke in strokes:
        for start, end in zip(stroke[:-1], stroke[1:]):
            if start[0] == end[0]:
                for y in range(min(start[1], end[1]), max(start[1], end[1])+1):
                    grid[start[0], y] = WALL
            else:
                for x in range(min(start[0], end[0]), max(start[0], end[0])+1):
                    grid[x, start[1]] = WALL
    return grid 


def fall(grid: np.array) -> np.array:
    while True:
        x, y = 500, 0

        while True:
            if y + 1 == grid.shape[1]:
                # Finish
                return grid
            elif grid[x,y+1] == NOTHING:
                y += 1
            else:
                if grid[x-1, y+1] == NOTHING:
                    x -= 1
                    y += 1
                elif grid[x+1, y+1] == NOTHING:
                    x += 1
                    y += 1
                else:
                    grid[x, y] = SAND
                    break
    return grid


def draw(grid: np.array):
    # nx, ny = grid.shape
    for y in range(0, 12):
        for x in range(470, 530):
            if grid[x,y] == NOTHING:
                print('.', end='')
            elif grid[x,y] == WALL:
                print('#', end='')
            else:
                print('o', end='')
        print('')

EXAMPLE = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip()

# draw(fall(parse(EXAMPLE)))

def part1(s: str) -> int:
    grid = parse(s)
    grid = fall(grid)
    return (grid == SAND).sum()


def fall2(grid: np.array) -> np.array:
    while grid[500, 0] == NOTHING:
        x, y = 500, 0

        while True:
            if grid[x,y+1] == NOTHING:
                y += 1
            else:
                if grid[x-1, y+1] == NOTHING:
                    x -= 1
                    y += 1
                elif grid[x+1, y+1] == NOTHING:
                    x += 1
                    y += 1
                else:
                    grid[x, y] = SAND
                    break
    return grid


def part2(s: str) -> int:
    grid = parse(s)

    # Find the max y
    max_y = -1   
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x,y] == WALL:
                max_y = max(y, max_y)
    for x in range(grid.shape[0]):
        grid[x, max_y+2] = WALL
    
    grid = fall2(grid)

    # draw(grid)
    return (grid == SAND).sum()


assert part1(EXAMPLE) == 24
assert part2(EXAMPLE) == 93

with open('inputs/day14.txt') as f:
    s = f.read()

print('part1', part1(s))
print('part2', part2(s))

