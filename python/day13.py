from typing import *
import enum


class Type(enum.Enum):
    INT = 0
    LIST = 1


class Var:

    def __init__(self, type_: Type, int_value: Optional[int] = None, list_value: Optional[list['Var']] = None) -> None:
        self.type_ = type_
        self.int_value = int_value
        self.list_value = list_value
        if self.type_ == Type.INT:
            self.list_value = [self.int_value]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.type_ == Type.INT:
            return str(self.int_value)
        else:
            return '[' + ','.join([str(x) for x in self.list_value]) + ']'

    def __lt__(self, other: 'Var') -> bool:
        return compare(self, other) < 0


class TokenReader:

    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.loc = 0

    def peek(self) -> str:
        return self.tokens[self.loc]

    def next(self) -> str:
        res = self.peek()
        self.loc += 1
        return res

    def has_next(self) -> bool:
        return self.loc < len(self.tokens)


def tokenize(s: str) -> TokenReader:
    import re
    parts = re.split(r'(\[|,|\])', s)
    return TokenReader([tkn for tkn in parts if tkn])


def do_parse(tokens: TokenReader) -> Var:
    tkn = tokens.next()
    if tkn.isdigit():
        return Var(Type.INT, int_value=int(tkn))
    elif tkn == '[':
        children = []
        while tokens.has_next():
            tkn = tokens.peek()
            if tkn == ']':
                tokens.next()
                break
            elif tkn == ',':
                tokens.next()
                continue
            else:
                c = do_parse(tokens)
                children.append(c)
        return Var(Type.LIST, list_value=children)
    else:
        RuntimeError('Parse error')


def parse(s: str) -> Var:
    tokens = tokenize(s)
    return do_parse(tokens)


def compare(left: Var, right: Var, depth=0, verbose=False) -> int:
    if verbose:
        indent = '  ' * depth
        print(indent + f'- Compare {left} vs {right}')

    if left.type_ == Type.INT and right.type_ ==Type.INT:
        if left.int_value < right.int_value:
            return -1
        elif left.int_value == right.int_value:
            return 0
        else:
            return 1
    elif left.type_ == Type.INT and right.type_ == Type.LIST:
        new_left = Var(Type.LIST, list_value=[left])
        return compare(new_left, right, depth=depth+1, verbose=verbose)
    elif left.type_ == Type.LIST and right.type_ == Type.INT:
        new_right = Var(Type.LIST, list_value=[right])
        return compare(left, new_right, depth=depth+1, verbose=verbose)
    else:
        n = min(len(left.list_value), len(right.list_value))
        for i in range(n):
            c = compare(left.list_value[i], right.list_value[i], depth=depth+1, verbose=verbose)
            if c == 0:
                continue
            else:
                return c
        if len(left.list_value) == len(right.list_value):
            return 0
        elif len(left.list_value) < len(right.list_value):
            return -1
        else:
            return 1


def part1(s: str, verbose=False) -> int:
    ans = 0
    for i, sub_problem in enumerate(s.split('\n\n'), 1):
        pieces = sub_problem.strip().split('\n')
        left = parse(pieces[0])
        right = parse(pieces[1])
        if verbose:
            print()
            print(f'== Pair {i} ==')
        if compare(left, right, verbose=verbose) == -1:
            ans += i
            if verbose:
                print('In the right order:', i)
    return ans


def part2(s: str) -> int:
    packets = [parse(line) for line in s.split('\n') if line]
    packets.append(parse('[[2]]'))
    packets.append(parse('[[6]]'))

    packets.sort()
    
    lines = [str(x) for x in packets] 
    ans = 1
    for i, line in enumerate(lines, 1):
        if line == '[[2]]':
            ans *= i
        elif line == '[[6]]':
            ans *= i
    return ans


EXAMPLE="""
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()

assert part1(EXAMPLE, verbose=True) == 13
assert part2(EXAMPLE) == 140

with open('inputs/day13.txt') as f:
    s = f.read()
print('part1', part1(s))
print('part2', part2(s))