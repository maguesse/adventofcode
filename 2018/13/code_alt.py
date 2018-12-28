#!/usr/bin/env python
from collections import namedtuple

class Tile:
    def __init__(self, x, y, desc):
        self.x = x
        self.y = y
        self.has_cart = False

    @property
    def x(self):
        return self.x

    @x.setter
    def x(self, x):
        self.x = x

    @property
    def y(self):
        return self.x

    @y.setter
    def y(self, y):
        self.y = y

def load_input(filename):
    with open(filename, 'r') as ifp:
        lines = ifp.read().splitlines()
    return lines

tiles_type = {
    '|':'vertical',
    '-':'horizontal',
    '/':'right_turn',
    '\\':'left_turn',
    '+':'intersection',
    ' ': None,
}


carts_type = {
    'v':'down',
    '^':'up',
    '<':'left',
    '>':'right'
}

o = {
    'turn_left':{'up':'left', 'down':'right', 'left':'down', 'right':'up'},
    'turn_rigth':{'up':'right', 'down':'left', 'left':'up', 'right':'down'},
}
cart_tiles = [ '<', '>', 'v', '^' ]
tile_under_cart = {
    '<':'-',
    '>':'-',
    'v':'|',
    '>':'|',
}


def turn(orientation, turn):
    return o[turn][orientation]

def move(cart, tracks):
    x, y, orientation, next_turn = cart

    if orientation == 'up':
        y -= 1
    elif orientation == 'down':
        y += 1
    elif orientation == 'left':
        x -= 1
    else :
        x += 1

    next_pos = tracks[y][x]
    print(next_pos.type)
    if next_pos.type in ['turn_left', 'turn_rigth']:
        import pdb;pdb.set_trace()
        orientation = turn(orientation, next_pos.type)
    elif next_pos.type == 'intersection':
        orientation = turn(orientation, next_turn)
        if next_turn == 'turn_left':
            next_turn = 'straigth'
        elif next_turn == 'staight':
            next_turn = 'turn_right'
        else:
            next_turn = 'turn_left'

    print(f'{cart} -> {(x, y, orientation, next_turn)}')
    return (x, y, orientation, next_turn)

def is_cart(tile):
    return tile in cart_tiles

def process(filename):
    part1 =  part2 = None
    tiles = load_input(filename)
    height = len(tiles)
    width = max([len(c) for c in tiles])
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if is_cart(tile):
                print(f'Cart @{x},{y}')


    #Tile = namedtuple('Tile','type')

    #tracks_map = [[None for _ in range(width)] for _ in range(height)]
    #carts = []
    ## Initialisation
    #for y, row in enumerate(tiles):
    #    for x, tile in enumerate(row):
    #        try:
    #            tracks_map[y][x] = Tile._make([tiles_type[tile]])
    #        except KeyError:
    #            carts.append((x, y, carts_type[tile], 'turn_left'))
    #            if carts_type[tile] in ['v', '^']:
    #                tracks_map[y][x] = Tile._make(['vertical'])
    #            else:
    #                tracks_map[y][x] = Tile._make(['horizontal'])

    #for tick in range(2):
    #    for i, cart in enumerate(carts):
    #        carts[i] = move(cart, tracks_map)

    return (part1, part2)

if __name__ == '__main__':
    print(process('test.txt'))
    #print(process('input'))
