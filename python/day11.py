from typing import *
import collections
import numpy as np

EXAMPLE = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()


class Monkey:

    def __init__(self, items: list[int], operation: str, test_divisor: int,
                 monkey_true: int, monkey_false: int) -> None:
        self.items = collections.deque(items)
        self.operation = operation
        self.test_divisor = test_divisor
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
#

    def do_operation(self, x) -> int:
        a, op, b = self.operation.split()
        a = x if a == 'old' else int(a)
        b = x if b == 'old' else int(b)
        if op == '*':
            return a * b
        elif op == '+':
            return a + b
        else:
            raise NotImplementedError()

    def inspect(self) -> list[tuple[int, int]]:
        res = []
        while self.items:
            x = self.items.popleft()
            x = self.do_operation(x)
            x //= 3
            if x % self.test_divisor == 0:
                res.append((self.monkey_true, x))
            else:
                res.append((self.monkey_false, x))
        return res

    def add_item(self, x: int) -> None:
        self.items.append(x)


def do_round(monkeys: list[Monkey]) -> list[int]:
    inspect_counts = np.array([0] * len(monkeys))
    for i, monkey in enumerate(monkeys):
        inspect_counts[i] = len(monkey.items)
        thrown_items = monkey.inspect()
        for index, worry_level in thrown_items:
            monkeys[index].add_item(worry_level)

    # for i in range(len(monkeys)):
    #     print('Monkey {}: {}'.format(i, ', '.join(map(str, monkeys[i].items))))
    return inspect_counts


def do_rounds(monkeys: list[Monkey], nround: int) -> int:
    inspect_counts = np.zeros((len(monkeys),), dtype=int)
    for r in range(1, 1+nround):
        inspect_counts += do_round(monkeys)
        for monkey in monkeys:
            n = len(monkey.items)
            for _ in range(n):
                x = monkey.items.popleft()
                monkey.items.append(x)
    print(inspect_counts)
    inspect_counts = sorted(inspect_counts)
    return inspect_counts[-1] * inspect_counts[-2]


def part1(s: str) -> int:
    monkeys = parse(s)
    return do_rounds(monkeys, 20)


def parse(s: str) -> list[Monkey]:
    res = []
    for part in s.strip().split('\n\n'):
        lines = part.strip().split('\n')
        items = [int(x.strip()) for x in lines[1].split(':')[1].split(',')]
        operation = lines[2].split('new = ')[1].strip()
        test_divisor = int(lines[3].split('divisible by ')[1].strip())
        true_monkey = int(lines[4].split('monkey')[1].strip())
        false_monkey = int(lines[5].split('monkey')[1].strip())
        res.append(Monkey(items, operation, test_divisor,
                   true_monkey, false_monkey))
    return res


class Monkey2(Monkey):

    def __init__(self, items: list[int], operation: str, test_divisor: int,
                 monkey_true: int, monkey_false: int) -> None:
        super().__init__(items, operation, test_divisor, monkey_true, monkey_false)
        self.items = collections.deque(items)
        self.operation = operation
        self.test_divisor = test_divisor
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.mods = None
        self.mod_idx = None

    def inspect(self) -> list[tuple[int, int]]:
        res = []
        while self.items:
            x = self.items.popleft()
            x = self.do_operation(x)
            r = x % self.mods
            if r[self.mod_idx] == 0:
                res.append((self.monkey_true, x))
            else:
                res.append((self.monkey_false, x))
        return res

    def add_item(self, x) -> None:
        self.items.append(x % self.mods)


def do_rounds2(monkeys: list[Monkey], nround: int) -> int:
    inspect_counts = np.zeros((len(monkeys),), dtype=int)
    for r in range(1, 1+nround):
        # print(r)
        inspect_counts += do_round(monkeys)
        for monkey in monkeys:
            n = len(monkey.items)
            for _ in range(n):
                x = monkey.items.popleft()
                monkey.items.append(x)
    print(inspect_counts)
    inspect_counts = sorted(inspect_counts)
    return inspect_counts[-1] * inspect_counts[-2]


def part2(s: str) -> int:
    monkeys = parse2(s)
    np.array([monkey.test_divisor for monkey in monkeys])
    for i, monkey in enumerate(monkeys):
        monkey.mods = np.array([monkey.test_divisor for monkey in monkeys])
        monkey.mod_idx = i

    return do_rounds2(monkeys, 10000)


def parse2(s: str) -> list[Monkey2]:
    res = []
    for part in s.strip().split('\n\n'):
        lines = part.strip().split('\n')
        items = [int(x.strip()) for x in lines[1].split(':')[1].split(',')]
        operation = lines[2].split('new = ')[1].strip()
        test_divisor = int(lines[3].split('divisible by ')[1].strip())
        true_monkey = int(lines[4].split('monkey')[1].strip())
        false_monkey = int(lines[5].split('monkey')[1].strip())
        res.append(Monkey2(items, operation, test_divisor,
                   true_monkey, false_monkey))
    return res


assert part1(EXAMPLE) == 10605
assert part2(EXAMPLE) == 2713310158

with open('inputs/day11.txt') as f:
    s = f.read()

print(part1(s))
print(part2(s))
