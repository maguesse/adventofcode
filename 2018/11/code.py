#!/usr/bin/env python

from functools import partial, lru_cache

@lru_cache(maxsize=900)
def cell_power(serial, x, y):
    rackid = x + 10
    return int(str(((rackid * y) + serial) * rackid)[-3]) - 5


def summed_area_table(width, height, func):
    psa = [[0 for _ in range(width + 1)] for _ in range(height + 1)]
    for y in range(height + 1):
        for x in range(width + 1):
            if x > 0 and y > 0:
                psa[y][x] = func(x, y) + psa[y-1][x] + psa[y][x-1] - psa[y-1][x-1]
    return psa

def sum_square_area(area, x, y, size):
    dx, dy = (x - 1, y - 1)
    return (area[dy + size][dx + size]
            + area[dy][dx]
            - area[dy][dx + size]
            - area[dy + size][dx])

def generate_power_area(serial_num, width, height):
    cell_power_serial = partial(cell_power, serial_num)
    power_area = []
    for y in range(1, height - 2):
        for x in range(1, width - 2):
            r = [sum([cell_power_serial(x + i, y + j)
                      for i in range(3)]) for j in range(3)]
            power_area.append((sum(r), (x, y)))
    return power_area

def process(serial_num, width, height):
    pa = generate_power_area(serial_num, width, height)
    max_power = max(pa)
    return f'{max_power[1][0]},{max_power[1][1]}'

def process_2(serial_num, width, height):
    cps = partial(cell_power, serial_num)
    sat = summed_area_table(width, height, cps)
    ssa = partial(sum_square_area, sat)
    squares = []
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            if x < y:
                max_size = height + 1- y
            else:
                max_size = width + 1 - x
            for s in range(max_size):
                squares.append((ssa(x, y, s), (x, y), s))

    largest = max(squares)
    return (largest[1][0], largest[1][1], largest[2])

if __name__ == '__main__':
    assert 4 == cell_power(8, 3, 5)
    assert -5 == cell_power(57, 122, 79)
    assert 0 == cell_power(39, 217, 196)
    assert 4 == cell_power(71, 101, 153)
    assert '33,45' == process(18, 300, 300)
    assert '21,61' == process(42, 300, 300)
    print(f'Part 1 solution : {process(7400, 300, 300)}')
    assert 30 == sum_square_area(summed_area_table(300, 300, partial(cell_power, 42)),
                             21, 61,3)
    assert 113 == sum_square_area(summed_area_table(300, 300, partial(cell_power, 18)),
                             90, 269,16)
    assert 119 == sum_square_area(summed_area_table(300, 300, partial(cell_power, 42)),
                             232, 251, 12)
    assert (90,269,16) == process_2(18, 300, 300)
    assert (232,251,12) == process_2(42, 300, 300)
    print(f'Part 2 solution: {process_2(7400, 300, 300)}')
