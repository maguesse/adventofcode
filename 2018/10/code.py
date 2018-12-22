#!/usr/bin/env python
import re
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'vx', 'vy'])

def process(data, factor=1, visualize=False):
    points = [Point._make(p) for p in data]
    min_area=10**15
    local_min_reached = False
    local_min = -1
    candiate = []
    for i in range(200000):
        move = [(x + i * vx, y + i * vy) for (x, y, vx, vy) in points]
        xmin = min(move, key=lambda s: s[0])[0]
        xmax = max(move, key=lambda s: s[0])[0]
        ymin = min(move, key=lambda s: s[1])[1]
        ymax = max(move, key=lambda s: s[1])[1]
        h = ymax - ymin
        w = xmax - xmin
        a = h * w
        if a < min_area:
            local_min_reached = True
            local_min = i
            min_area = a
        else:
            break

    print(f'Local minimum found @{local_min}')

    if visualize:
        candidate = [(x + local_min * vx, y + local_min * vy) for (x, y, vx, vy) in
                 points]
        xmin = min(candidate, key=lambda s: s[0])[0]
        xmax = max(candidate, key=lambda s: s[0])[0]
        ymin = min(candidate, key=lambda s: s[1])[1]
        ymax = max(candidate, key=lambda s: s[1])[1]
        xoffset = 0 - xmin
        yoffset = 0 - ymin
        xmin = (xmin + xoffset)
        xmax = (xmax + xoffset)
        ymin = (ymin + yoffset)
        ymax = (ymax + yoffset)
        candidate = [(x + xoffset, y + yoffset) for (x, y) in
                 candidate]
        for y in range(ymin, ymax+1):
            row = ['.' for _ in range(xmin, xmax + 1)]
            for p in [c for c in candidate if c[1] == y]:
                row[p[0]] = '#'
            print(''.join(row))

def load_input(filename):
    points_ptn = re.compile('(-?\d+)')
    return list(tuple([int(s) for s in points_ptn.findall(line)])
                for line in open(filename, 'r').read().splitlines())

if __name__=='__main__':
    process(load_input('test.txt'), factor=1, visualize=True)
    print('\n'+ '*'*80 +'\n')
    process(load_input('input'), factor=1, visualize=True)
