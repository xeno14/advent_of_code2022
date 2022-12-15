import re
import numpy as np

Point = tuple[int, int]


def parse(s: str) -> tuple[list[Point], list[Point]]:
    pattern = re.compile(r"x=(-?\d+), y=(-?\d+)")
    sensors = []
    beacons = []

    for line in s.split('\n'):
        (sx, sy), (bx, by) = pattern.findall(line) 
        sensors.append((int(sx), int(sy)))
        beacons.append((int(bx), int(by)))
    return sensors, beacons


def manhattan(a: Point, b: Point) -> int:
    return abs(a[0]-b[0]) + abs(a[1] - b[1])


def part1(s: str, y: int) -> int:
    sensors, beacons = parse(s)
    distances = [manhattan(s, b) for s, b in zip(sensors, beacons)]

    sensor_set = set(sensors)
    beacon_set = set(beacons)
    void_set = set()

    for i in range(len(sensors)):
        s = sensors[i]
        d = distances[i]

        dy = abs(s[1] - y)
        dx = d - dy

        # too far.
        if dx <=0:
            continue

        for x in range(s[0]-dx, s[0]+dx+1):
            void_set.add((x, y))

    void_set -= beacon_set

    return len(void_set)


def find_range(sensors: list[Point], distances: list[int], y: int, size: int) -> list[tuple[int, int]]:
    ranges = list()
    for s, d in zip(sensors, distances):
        dx = d - abs(s[1] - y)
        if dx <= 0:
            continue

        first = max(s[0]-dx, 0)
        last = min(s[0]+dx, size)

        ranges.append((first, last))
    # merge
    if len(ranges)==1:
        return ranges
    ranges.sort()   
    res = [ranges[0]]
    for rng in ranges[1:]:
        last_rng = res[-1]
        if last_rng[1] >= rng[0]:
            res.pop()
            res.append((last_rng[0], max(last_rng[1], rng[1])))
        else:
            res.append(rng)
    return res


def part2(s: str, size: int) -> int:
    sensors, beacons = parse(s)
    distances = [manhattan(s, b) for s, b in zip(sensors, beacons)]

    for y in range(0, size+1):
        if y % 100000==0:
            print(f'{y=}')
        rng = find_range(sensors, distances, y=y, size=size)
        if len(rng) != 1:
            x = rng[0][1] + 1
            return 4000000 * x + y
    raise RuntimeError('no distress signal found')


EXAMPLE = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip()

assert part1(EXAMPLE, y=10) == 26
assert part2(EXAMPLE, size=20) == 56000011

with open('inputs/day15.txt') as f:
    s = f.read()

print('part1', part1(s, y=2000000))
print('part2', part2(s, size=4000000))

