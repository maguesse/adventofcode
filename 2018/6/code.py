#!/usr/bin/env python
import csv
import math
import random
from PIL import Image

class Coord:
    def __init__(self, x, y):
        self.__x = int(x)
        self.__y = int(y)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    def __repr__(self):
        return f'<Coord x:{self.x}, y:{self.y}>'

class Site(Coord):

    def __init__(self, id, x, y, size=0, infinite=False):
        Coord.__init__(self, x, y)
        self.__id = id
        self.__size = size
        self.__infinite = infinite

    @property
    def id(self):
        return self.__id

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

    @property
    def infinite(self):
        return self.__infinite

    @infinite.setter
    def infinite(self, infinite):
        if self.__infinite == False:
            self.__infinite = infinite


    def inc_size(self):
        self.__size += 1

    def dec_size(self):
        self.__size -= 1

    def __repr__(self):
        return (
            f'<Site id:{self.id} x:{self.x}, y:{self.y}, size:{self.size},'
        f'infinite:{self.infinite}>')


class Point(Coord):
    def __init__(self, x, y) :
        Coord.__init__(self, x, y)
        self.__site = None
        self.__is_edge = False

    @property
    def site(self):
        return self.__site

    @site.setter
    def site(self, site):
        self.__site = site

    @property
    def is_edge(self):
        return self.__is_edge

    @is_edge.setter
    def is_edge(self, is_edge):
        self.__is_edge = is_edge


    def __repr__(self):
        return (f'<Point x:{self.x}, y:{self.y},'
                f'site:{self.site}'
                f', is_edge:{self.is_edge}'
                '>')


def load_input(input_file):
    return [Site(id, line[0], line[1]) for id, line
            in enumerate(csv.reader(open(input_file,'r'),
                          skipinitialspace=True))]


def euclidian_distance(coord1, coord2):
    return math.sqrt((coord1.x - coord2.x)**2
                     + (coord1.y - coord2.y)**2)

def manhattan_dist(coord1, coord2):
    return abs(coord1.x - coord2.x) + abs(coord1.y - coord2.y)

def is_edge(coord, width, height):
    return (coord.x == 0
            or coord.x == width
            or coord.y == 0
            or coord.y == height)

def get_solutions(sites, dist):
    # Find box region
    min_x = min(sites, key=lambda p: p.x).x
    max_x = max(sites, key=lambda p: p.x).x
    min_y = min(sites, key=lambda p: p.y).y
    max_y = max(sites, key=lambda p: p.y).y

    nb_sites = len(sites)
    width = max_x
    height = max_y
    _dmin = dist(Coord(0, 0), Coord(width, height))

    world = [[None for x in range(width+1)]
             for y in range(height+1)]

    for y in range(height+1):
        for x in range(width+1):
            this_point = Point(x, y)
            this_point.is_edge = is_edge(this_point, width, height)
            dmin = _dmin
            for site in sites:
                d = dist(site, this_point)
                if d <= dmin:
                    dmin = d
                    if (not this_point.site
                        or d < this_point.site[0]):
                            this_point.site = (d, site)
                    elif d == this_point.site[0]:
                        this_point.site = None

            world[y][x] = this_point

    for line in world:
        for point in line:
            if point.site:
                this_site = sites[sites.index(point.site[1])]
                this_site.inc_size()
                this_site.infinite = point.is_edge


    area = max([site for site in sites if not site.infinite], key=lambda x:
              x.size).size

    return area, None

    '''
    colors = [(random.randrange(256),
               random.randrange(256),
               random.randrange(256)) for i in range(nb_sites)]
    image = Image.new('RGB', (width,height))
    putpixel = image.putpixel
    for line in world:
        for point in line:
            putpixel((point.x, point.y), 
                     (lambda x: colors[x[1].id] if x else (0,0,0))(point.site))
    image.show()
    image.save('test.png')
    '''

def process(sites):
    p1, p2 = get_solutions(sites, manhattan_dist)


    print('Result for part one is {}.'.format(p1))
    print('Result for part two is {}.'.format(p2))

if __name__ == "__main__":
    process(load_input('test.txt'))
    #process(load_input('input'))
