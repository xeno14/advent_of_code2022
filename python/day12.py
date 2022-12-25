import numpy as np
import collections

EXAMPLE="""
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()


def parse(s: str) -> tuple[tuple[int,int], tuple[int,int], np.array]:
    rows = []
    for i, line in enumerate(s.split('\n')):
        row = []
        for j in range(len(line)):
            c = line[j]
            if c == 'S':
                start = (i, j)
                c = 'a'
            elif c == 'E':
                c = 'z'
                end = (i, j)
            row.append(ord(c))
        rows.append(row)
    return start, end, np.array(rows)


def find_shortest(start, end, elev: np.array) -> int:
    dist = np.zeros(elev.shape, dtype=int)

    q = collections.deque()
    q.append(start)
    while q:
        cur = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            x = cur[0] + dx
            y = cur[1] + dy
            if x < 0 or x >= dist.shape[0] or y < 0 or y >= dist.shape[1]:
                continue
            if dist[x, y] > 0:  # already visited
                continue
            if elev[x,y] > elev[cur] + 1:  # unable to move
                continue
            dist[x,y] = dist[cur] + 1
            q.append((x, y))

            if x==end[0] and y==end[1]:
                return dist[x, y]
    raise RuntimeError('End not found.')



def part1(s : str) ->int:
    start, end, elev = parse(s)
    return find_shortest(start, end, elev)


def part2(s : str) ->int:
    _, end, elev = parse(s)
    ans = 1<<20
    for i in range(elev.shape[0]):
        for j in range(elev.shape[1]):
            e = elev[i,j]
            print(f'({i}, {j}) in {elev.shape}')
            if e == ord('a'):
                try:
                    ans = min(ans, find_shortest((i,j), end, elev))
                except RuntimeError:
                    continue
    return ans


assert part1(EXAMPLE) == 31
assert part2(EXAMPLE) == 29
    
with open('inputs/day12.txt') as f:
    s = f.read()
print(part1(s))
print(part2(s))
