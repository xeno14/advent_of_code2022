EXAMPLE="""
1=-0-2
 12111
  2=0=
    21
  2=01
   111
 20012
   112
 1=-1=
  1-12
    12
    1=
   122
""".strip()


def snafu2dec(s: str) -> int:
    res = 0
    n=1
    for c in reversed(s):
        if c == '=':
            res -= 2 * n
        elif c == '-':
            res -= n
        elif c == '1':
            res += n
        elif c == '2':
            res += 2*n
        n *= 5
    return res


def dec2snafu(n: int) -> str:
    # dec2quin
    digits = []
    while n:
        digits.append(n%5)
        n //= 5
    digits.append(0)
    # print(digits)
    
    pieces = []
    DIGIT_MAP = {
                -2: '=',
                -1: '-',
                0: '0',
                1: '1',
                2: '2',
    }
    for i in range(len(digits)):
        n = digits[i]
        if 0 <= n <= 2:
            pieces.append(DIGIT_MAP[n])
        elif 3 <= n <= 5:
            digits[i+1] += 1
            pieces.append(DIGIT_MAP[n-5])
        else:
            raise RuntimeError('???')
    if len(pieces) > 1 and pieces[-1] == '0':
        pieces.pop()
    return ''.join(reversed(pieces))


def part1(s: str) -> str:
    n = sum(map(snafu2dec, s.split('\n')))
    return dec2snafu(n)


assert snafu2dec('1=-0-2') == 1747
assert snafu2dec('12111') == 906
assert snafu2dec('2=0=') == 198
assert snafu2dec('21') == 11
assert snafu2dec('2=01') == 201
assert snafu2dec('111') == 31
assert snafu2dec('20012') ==1257
assert snafu2dec('112') == 32
assert snafu2dec('1=-1=') == 353
assert snafu2dec('1-12') == 107
assert snafu2dec('12') == 7
assert snafu2dec('1=') == 3
assert snafu2dec('122') == 37

assert part1(EXAMPLE) == '2=-1=0'

with open('inputs/day25.txt') as f:
    s = f.read()

print('part1', part1(s))
