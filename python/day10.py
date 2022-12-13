

EXAMPLE="""
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".strip()


def run(code: str) -> list[int]:
    regs = [1]
    for line in code.split('\n'):
        reg = regs[-1]
        if line == 'noop':
            regs.append(reg)
        else:
            val = int(line.split()[1])
            regs.append(reg)
            regs.append(reg + val)
    return regs


def part1(code: str) -> int:
    regs = run(code)
    idx = [20, 60, 100, 140, 180, 220]
    ans = 0
    for i in idx:
        a = i * regs[i-1]
        print(f'cycle={i} * reg={regs[i]} = {a}')
        ans += a

    return ans


def part2(code: str) -> int:
    regs = run(code)
    print(regs)

    for cycle in range(240):
        draw_pos = cycle % 40
        sprite_mid = regs[cycle]

        if sprite_mid - 1 <= draw_pos <= sprite_mid + 1:
            print('#', end='')
        else:
            print('.', end='')
        if (cycle+1)%40==0:
            print()
        
        
    # idx = [20, 60, 100, 140, 180, 220]
    # ans = 0
    # for i in idx:
    #     a = i * regs[i-1]
    #     print(f'cycle={i} * reg={regs[i]} = {a}')
    #     ans += a

    # return ans


print(run("""
noop
addx 3
addx -5
""".strip()))  

assert part1(EXAMPLE) == 13140
part2(EXAMPLE)

with open('inputs/day10.txt') as f:
    s = f.read()

print('part1', part1(s))
part2(s)
