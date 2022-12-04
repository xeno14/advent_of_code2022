import dataclasses
from typing import *

@dataclasses.dataclass
class Range:
    left: int
    right: int

    def fully_contains(self, other: 'Range') -> bool:
        return self.left <= other.left and other.right <= self.right

    def overwraps(self, other: 'Range') -> bool:
        return (self.left <= other.left <= self.right) or (self.left <= other.right <= self.right)

    @staticmethod
    def parse_from_string(s: str) -> 'Range':
        left, right = s.split('-')
        return Range(int(left), int(right))



EXAMPLE="""
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip()


def parse(s: str) -> List[Tuple[Range, Range]]:
    res = []
    for line in s.strip().split():
        if not line:
            continue
        x, y = line.split(',')
        res.append((Range.parse_from_string(x), Range.parse_from_string(y)))
    return res


def part1(s: str) -> int:
    range_pairs = parse(s)
    ans = 0
    for x, y in range_pairs:
        ans += (x.fully_contains(y) or y.fully_contains(x))
    return ans


def part2(s: str) -> int:
    range_pairs = parse(s)
    ans = 0
    for x, y in range_pairs:
        ans += (x.overwraps(y) or y.overwraps(x))
    return ans



assert part1(EXAMPLE) == 2
assert part2(EXAMPLE) == 4
with open('inputs/day4.txt') as f:
    s = f.read()
print(part1(s))
print(part2(s))
