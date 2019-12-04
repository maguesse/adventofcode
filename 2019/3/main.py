import util
import re

def manhattan_dist(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def move_up(pos):
    return (pos[0]    , pos[1] + 1)

def move_down(pos):
    return (pos[0]    , pos[1] - 1)

def move_right(pos):
    return (pos[0] + 1, pos[1]    )

def move_left(pos):
    return (pos[0] - 1, pos[1]    )

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
            pos = NEXT_POS[dir[0]](pos)
            res.append(pos)
    return res

def find_intersections(data):
    data = get_dirs(data)
    routes = [compute_route(d) for d in data]
    intersections = [(manhattan_dist((0,0), x), x) for x 
                     in set(routes[0]) & set(routes[1])]
    return (routes, intersections)

def part1(data):
    routes, intersections = find_intersections(data)
    return min(intersections, key=lambda x: x[0])[0]

def part2(data):
    routes, intersections =  find_intersections(data)
    return min([sum([r.index(i[1]) + 1 for r in routes]) for i in intersections])

def get_dirs(data):
    points_ptn = re.compile('([RLUD])(\d+)')
    return [[points_ptn.match(i).groups() for i in line] for line in data]

def solve(part):
    data = util.load_lists_of_strings()
    print(f'{part.__name__} : {part(data)}')



if __name__ == '__main__':
    split = lambda s: s.split(',')
    ex1 = list(map(split, ['R8,U5,L5,D3',
                      'U7,R6,D4,L4']))
    ex2 = list(map(split, ['R75,D30,R83,U83,L12,D49,R71,U7,L72',
                      'U62,R66,U55,R34,D71,R55,D58,R83']))
    ex3 = list(map(split, ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
                      'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']))
    assert 6 == part1(ex1)
    assert 159 == part1(ex2)
    assert 135 == part1(ex3)
    solve(part1)
    assert 30 == part2(ex1)
    assert 610 == part2(ex2)
    assert 410 == part2(ex3)
    solve(part2)
