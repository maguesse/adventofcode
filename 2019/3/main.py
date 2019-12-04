import util
import re


def manhattan_dist(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def move_up(pos, length):
    return (pos[0], pos[1]+length)

def move_down(pos, length):
    return (pos[0], pos[1]-length)

def move_right(pos, length):
    return (pos[0] + length, pos[1])

def move_left(pos, length):
    return (pos[0] - length, pos[1])

NEXT_POS = {
    'U': move_up,
    'D': move_down,
    'L': move_left,
    'R': move_right,
}

def compute_route(dirs):
    pos = (0,0)
    res = []
    for dir in dirs:
        length = int(dir[1])
        rng = range(length)
        for r in rng:
            if dir[0] == 'U':
                pos = (pos[0], pos[1]+1)
            elif dir[0] == 'D':
                pos = (pos[0], pos[1]-1)
            elif dir[0] == 'L':
                pos = (pos[0]-1, pos[1])
            elif dir[0] == 'R':
                pos = (pos[0]+1, pos[1])
            res.append(pos)
    return set(res)



def part1(data):
    data = get_dirs(data)
    routes = [compute_route(d) for d in data]
    return min([manhattan_dist((0,0), x) for x in routes[0] & routes[1]])


def get_dirs(data):
    points_ptn = re.compile('([RLUD])(\d+)')
    return [[points_ptn.match(i).groups() for i in line] for line in data]

def solve():
    data = util.load_lists_of_strings()
    print(f'Part 1 : {part1(data)}')


if __name__ == '__main__':
    split = lambda s: s.split(',')
    assert 6 == part1(map(split,
                          ['R8,U5,L5,D3',
                           'U7,R6,D4,L4']))
    assert 159 == part1(map(split,
        ['R75,D30,R83,U83,L12,D49,R71,U7,L72',
         'U62,R66,U55,R34,D71,R55,D58,R83']))
    assert 135 == part1(map(split,
                            ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
                             'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']))
    solve()
