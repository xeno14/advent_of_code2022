import numpy as np
import itertools


ROCKS = [
    np.array([
        [1, 1, 1, 1]
    ], dtype=int),
    np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ], dtype=int),
    np.array([
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
    ], dtype=int),
    np.array([
        [1],
        [1],
        [1],
        [1],
    ], dtype=int),
    np.array([
        [1, 1],
        [1, 1],
    ], dtype=int),
]


def has_contact_down(board, rock, x, y):
    ny, nx = rock.shape

    # attach the wall
    if y == 0:
        return True

    for dx in range(nx):
        for dy in range(ny):
            if rock[dy, dx] and board[y+dy-1, x+dx]:
                return True
    return False


def has_contact_right(board, rock, x, y):
    ny, nx = rock.shape

    # attach the wall
    if x + nx >= board.shape[1]:
        return True

    for dx in range(nx):
        for dy in range(ny):
            if rock[dy, dx] and board[y+dy, x+dx+1]:
                return True
    return False


def has_contact_left(board, rock, x, y):
    ny, nx = rock.shape

    # attach the wall
    if x - 1 < 0:
        return True

    for dx in range(nx):
        for dy in range(ny):
            if rock[dy, dx] and board[y+dy, x+dx-1]:
                return True
    return False


def do_print(board: np.array):
    max_height = sum(board.any(axis=1))
    rows = list(map(lambda row: ''.join(
        [('#' if c else '.') for c in row]), board[:max_height+10]))
    print('\n'.join(rows[::-1]))


def do_print_move(board: np.array, rock, x, y):
    board = board.copy()
    for dx in range(rock.shape[1]):
        for dy in range(rock.shape[0]):
            if rock[dy, dx]:
                board[y+dy, x+dx] = -1
    max_height = sum(board.any(axis=1))
    rows = list(map(lambda row: ''.join(
        [('#' if c > 0 else '@' if c < 0 else '.') for c in row]), board[:max_height+10]))
    print('\n'.join(rows[::-1]))


def fall(num_rocks: int, winds: str) -> tuple[np.array, int]:
    board = np.zeros((4 * num_rocks + 10, 7), dtype=int)
    rock_iter = itertools.cycle(ROCKS)
    wind_iter = itertools.cycle(winds)
    current_height = 0

    for rock_id in range(1, num_rocks+1):
        rock = next(rock_iter)
        x = 2
        y = current_height + 3

        # print()
        # do_print_move(board, rock, x, y)

        # Fall the rock.
        while True:
            # blow wind
            wind = next(wind_iter)
            if wind == '>' and not has_contact_right(board, rock, x, y):
                x += 1
            elif wind == '<' and not has_contact_left(board, rock, x, y):
                x -= 1

            # Check down.
            if has_contact_down(board, rock, x, y):
                ny, nx = rock.shape
                board[y:y+ny, x:x+nx] += (rock * rock_id)
                current_height = max(current_height, y + ny)
                break

            y -= 1

            # print()
            # do_print_move(board, rock, x, y)

    do_print(board)
    return board, current_height


def part1(s: str):
    board, current_height = fall(2022, s)
    return current_height


def make_key(rock_id, wind_id, board: np.array):
    board = board.copy()
    board[board > 0] = 1
    return (rock_id, wind_id, tuple(board.flatten()))


def fall2(num_rocks: int, winds: str) -> int:
    board = np.zeros((10000, 7), dtype=int)
    rock_iter = itertools.cycle(enumerate(ROCKS))
    wind_iter = itertools.cycle(enumerate(winds))
    current_height = 0
    current_height_offset = 0

    key_to_step_height = dict()

    remaining_steps = num_rocks
    step = 0

    while remaining_steps > 0:
        step += 1
        remaining_steps -= 1

        rock_id, rock = next(rock_iter)
        x = 2
        y = current_height + 3

        # Fall the rock.
        while True:
            # blow wind
            wind_id, wind = next(wind_iter)
            if wind == '>' and not has_contact_right(board, rock, x, y):
                x += 1
            elif wind == '<' and not has_contact_left(board, rock, x, y):
                x -= 1

            # Check down.
            if has_contact_down(board, rock, x, y):
                ny, nx = rock.shape
                board[y:y+ny, x:x+nx] += (rock * step)
                current_height = max(current_height, y + ny)
                break
            y -= 1

        # Settled. Check the patten is repeated.
        if current_height_offset == 0 and current_height > 10:
            # Look up the last 8 rows for pattern matching.
            top = board[current_height-8:current_height]
            key = make_key(rock_id, wind_id, top)
            if key in key_to_step_height:
                prev_step, prev_height = key_to_step_height[key]

                print(f'Key found! current step={step} previous (step, hegiht)'
                      f'={key_to_step_height[key]}')

                period = step - prev_step
                height_delta = current_height - prev_height
                n = remaining_steps // period
                remaining_steps %= period
                current_height_offset += n * height_delta
            else:
                key_to_step_height[key] = (step, current_height)

    # do_print(board)
    return current_height + current_height_offset


def part2(s: str) -> int:
    return fall2(1000000000000, s)


EXAMPLE = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'


assert part1(EXAMPLE) == 3068
assert part2(EXAMPLE) == 1514285714288

with open('inputs/day17.txt') as f:
    s = f.read()

print('part1', part1(s))
print('part2', part2(s))
