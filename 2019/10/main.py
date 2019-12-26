import util
import math

def slope(pos1, pos2):
    return math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0])

def detect(pos, field):
    return len({slope(pos, asteroid) for asteroid in field if asteroid!=pos})

def solve_part1(data):
    asteroids = [(x,y) for y, row in enumerate(data)
                 for x, cell in enumerate(row)
                 if cell == '#']
    return max([(asteroid, detect(asteroid, asteroids))
                    for asteroid in asteroids], key=lambda x: x[1])

def solve_part2(data):
    pass

def solve(Part2=False):
    data = util.load_data()
    if not Part2:
        res = solve_part1(data)
    else:
        res = solve_part2(data)

    print(f'Part {"2" if Part2 else "1"}: {res}')

if __name__ == '__main__':
    import pytest
    if pytest.main() == 0:
        solve()
        solve(Part2=True)
