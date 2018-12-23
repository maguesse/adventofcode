#!/usr/bin/env python

from functools import partial, lru_cache


@lru_cache(maxsize=900)
def power_level(serial, x, y):
    rackid = x + 10
    return int(str(((rackid * y) + serial) * rackid)[-3]) - 5

def process(serial_num, width, height):
    power_level_serial = partial(power_level, serial_num)
    power_cells = []
    for y in range(1, height - 2):
        for x in range(1, width - 2):
            r = [sum([power_level_serial(x + i, y + j)
                      for i in range(3)]) for j in range(3)]
            power_cells.append((sum(r), (x, y)))
    max_power = max(power_cells)
    return f'{max_power[1][0]},{max_power[1][1]}'

if __name__ == '__main__':
    assert 4 == power_level(8, 3, 5)
    assert -5 == power_level(57, 122, 79)
    assert 0 == power_level(39, 217, 196)
    assert 4 == power_level(71, 101, 153)
    assert '33,45' == process(18, 300, 300)
    assert '21,61' == process(42, 300, 300)

    print(f'Part 1 solution : {process(7400, 300, 300)}')
