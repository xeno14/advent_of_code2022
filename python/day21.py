from typing import *


EXAMPLE = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip()

import dataclasses
@dataclasses.dataclass
class Monkey:
    name: str
    val: Optional[int] = None
    op: Optional[str] = None
    lhs: Optional[str] = None
    rhs: Optional[str] = None


def calc(name, graph: dict[str, Monkey]) -> int:
    m = graph[name]
    if m.val is not None:
        return m.val
    else:
        lhs = calc(m.lhs, graph)
        rhs = calc(m.rhs, graph)
        if m.op == '+':
            val = lhs+rhs
        elif m.op=='-':
            val = lhs-rhs
        elif m.op=='/':
            val= lhs//rhs
        elif m.op=='*':
            val=lhs*rhs
        elif m.op =='=':
            if lhs < rhs:
                val = -1
            elif lhs > rhs:
                val = 1
            else:
                val = 0
            print(f'root: {lhs=} {rhs=}')
        else:
            raise RuntimeError('unknown operation', m.op)
        m.val = val
        return val
    

def parse(s: str) -> dict[str, Monkey]:
    g = {}
    for line in s.split('\n'):
        name, y = line.split(':')
        y = y.strip()
        m = Monkey(name)
        if y.isdigit():
            m.val = int(y)
        else:
            lhs, op, rhs = y.split()
            m.lhs = lhs
            m.op = op
            m.rhs = rhs
        g[name] = m
    return g


def part1(s:str) -> int:
    g = parse(s)
    return calc('root', g)


def calc2(s, humn) -> int:
    g = parse(s)
    g['root'].op = '='
    g['humn'].val = humn
    return calc('root', g)


def part2(s:str, low, high, sign=1)->int:
    while True:
        mid = (low + high) // 2
        cmp = calc2(s, mid) * sign
        if cmp < 0:
            low = mid
        elif cmp > 0:
            high = mid
        else:
            return mid


assert (part1(EXAMPLE) == 152)
print(part2(EXAMPLE, 0, 1000))

with open('inputs/day21.txt') as f:
    s=f.read()

print('part1', part1(s))

print(part2(s, low=1<<10, high=1<<60, sign=-1))
