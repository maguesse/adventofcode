#!/usr/bin/env python

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def manhattan_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def get_bounds(sites):
    xmin = min(sites, key=lambda s: s.x).x
    xmax = max(sites, key=lambda s: s.x).x
    ymin = min(sites, key=lambda s: s.y).y
    ymax = max(sites, key=lambda s: s.y).y
    return xmin, xmax, ymin, ymax

def is_edge(point, boundaries):
    return (point.x == boundaries[0]
            or point.x == boundaries[1]
            or point.y == boundaries[2]
            or point.y == boundaries[3])

def process(sites, dist_func, safe_distance = 10000):
    boundaries = get_bounds(sites)

    areas = [0 for s in sites]
    infinite = [False for s in sites]
    safe_region = 0
    for y in range(boundaries[2], boundaries[3]+1):
        for x in range(boundaries[0], boundaries[1]+1):
            this_point = Point(x, y)
            ds = [dist_func(site, this_point) for site in sites]
            dmin = min(ds)
            if ds.count(dmin) == 1:
                site_id = ds.index(dmin)
                candidate = sites[site_id]
                areas[site_id] += 1
                if (is_edge(candidate, boundaries)
                        or is_edge(Point(x,y), boundaries)):
                    infinite[site_id] = True
            if sum(ds) < safe_distance:
                safe_region +=1


    p1 = max([s for s in
               sorted(zip(areas, infinite), key=lambda x: x[0], reverse=True)
               if not s[1]
               ])[0]
    p2 = safe_region
    return p1, p2

def load_input(filename):
    return list((Point._make(map(int, line.split(',')))
                 for line in open(filename, 'r')))

if __name__=='__main__':
    print(process(load_input('test.txt'), manhattan_dist, 32))
    print(process(load_input('input'), manhattan_dist))
