import dataclasses
import collections
import math


EXAMPLE_SMALL="""
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
""".strip()

EXAMPLE = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".strip()

DELTAS = {
'>': (1, 0),
'v': (0, 1),
'<': (-1, 0),
'^': (0, -1),
}


@dataclasses.dataclass(frozen=True)
class Blizard:
    pos: tuple[int,int]
    direc: tuple[int, int]


def next_blizerd(blizards: set[Blizard], nx, ny):
    res: set[Blizard] = set()
    for b in blizards:
        res.add(
            Blizard(
                pos=((b.pos[0]+b.direc[0])%nx, (b.pos[1]+b.direc[1])%ny),
                direc=b.direc
            )
        )
    return res


def parse(s: str):
    lines = s.split('\n')
    ny = len(lines) - 2
    nx = len(lines[0])-2

    b = BlizardHolder(nx, ny)
    for y in range(1, ny+1):
        for x in range(1, nx+1):
            c = lines[y][x]
            if c in DELTAS:
                b.add(x-1, y-1, DELTAS[c][0], DELTAS[c][1])
    b.advance()
    return b, nx, ny


class BlizardHolder:

    def __init__(self, nx: int, ny: int):
        self.nx = nx
        self.ny = ny
        self.tmod = math.lcm(nx, ny)
        self.snapshots = [set()]
        self.pos_snapshots = [set()]
    
    def add(self, x, y, ux, uy):
        self.snapshots[0].add(
            Blizard(pos=(x,y), direc=(ux, uy)))
        self.pos_snapshots[0].add((x,y))
    
    def has(self, t, x, y):
        return (x, y) in self.pos_snapshots[t%self.tmod]

    def advance(self):
        for _ in range(self.tmod):
            b = next_blizerd(self.snapshots[-1], self.nx, self.ny)
            pos = set([x.pos for x in b])
            self.snapshots.append(b)
            self.pos_snapshots.append(pos)
    

def find_shortest(t, start, goal, nx, ny, blizard: Blizard) -> int:
    q = collections.deque([(start, t)])
    visited = set()

    while q:
        pos, t = q.popleft()
        if (pos, t%blizard.tmod) in visited:
            continue
        visited.add((pos, t%blizard.tmod))
        if pos == goal:
            return t-1
        for dx, dy in ((1, 0), (0, 1), (0, 0), (-1, 0), (0, -1)):
            npos = (pos[0]+dx, pos[1]+dy)
            if npos != start and npos != goal and (npos[0] < 0 or nx <= npos[0] or npos[1]<0 or ny <= npos[1]):
                continue
            if blizard.has(t, npos[0], npos[1]):
                continue
            else:
                q.append((npos, t+1))

    raise RuntimeError('Unreachable')


def part1(s: str) -> int:
    blizard, nx, ny = parse(s)
    return find_shortest(t=0, start=(0, -1), goal=(nx-1, ny), nx=nx, ny=ny, blizard=blizard)


def part2(s: str) -> int:
    blizard, nx, ny = parse(s)
    print('part2 start->goal')
    t1 = find_shortest(t=0, start=(0, -1), goal=(nx-1, ny), nx=nx, ny=ny, blizard=blizard)
    print('part2 goal->start')
    t2 = find_shortest(t=t1, goal=(0, -1), start=(nx-1, ny), nx=nx, ny=ny, blizard=blizard)
    print('part2 start->goal')
    t3 = find_shortest(t=t2, start=(0, -1), goal=(nx-1, ny), nx=nx, ny=ny, blizard=blizard)
    return t3


assert part1(EXAMPLE) == 18
assert part2(EXAMPLE) == 54

with open('inputs/day24.txt') as f:
    s = f.read()

print('part1', part1(s))
print('part2', part2(s))
