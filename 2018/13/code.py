#!/usr/bin/env python
class CollisionError(Exception):
    def __init__(self, x, y, message):
        self.x = x
        self.y = y
        self.message = message

def load_input(filename):
    with open(filename, 'r') as ifp:
        lines = ifp.read().splitlines()
    return [list(line) for line in lines]

CART_TILES = ['<', '>', 'v', '^']
TURN_TILES = ['\\', '/', '+']
TILE_UNDER_CART = {
    '<':'-',
    '>':'-',
    'v':'|',
    '^':'|',
}
NEXT_POS = {
    'v': lambda x, y: (x, y + 1),
    '^': lambda x, y: (x, y - 1),
    '<': lambda x, y: (x - 1, y),
    '>': lambda x, y: (x + 1, y),
}

def turn_on_slash(cart):
    ''' turn on / '''
    orientation = cart['tile']
    if orientation == '>':
        orientation = '^'
    elif orientation == '<':
        orientation = 'v'
    elif orientation == '^':
        orientation = '>'
    else:
        orientation = '<'
    cart['tile'] = orientation
    return cart

def turn_on_backslash(cart):
    ''' turn on \\ '''
    orientation = cart['tile']
    if orientation == '>':
        orientation = 'v'
    elif orientation == '<':
        orientation = '^'
    elif orientation == '^':
        orientation = '<'
    else:
        orientation = '>'
    cart['tile'] = orientation
    return cart

def turn_left(cart):
    orientation = cart['tile']
    if orientation == '>':
        orientation = '^'
    elif orientation == '<':
        orientation = 'v'
    elif orientation == '^':
        orientation = '<'
    elif orientation == 'v':
        orientation = '>'
    cart['tile'] = orientation
    return cart

def turn_right(cart):
    orientation = cart['tile']
    if orientation == '>':
        orientation = 'v'
    elif orientation == '<':
        orientation = '^'
    elif orientation == '^':
        orientation = '>'
    elif orientation == 'v':
        orientation = '<'
    cart['tile'] = orientation
    return cart

def turn_on_instersection(cart):
    turn = cart['turn']
    if turn == 0: #turn left
        cart = turn_left(cart)
    elif turn == 2: #turn right
        cart = turn_right(cart)
    cart['turn'] = (turn + 1) % 3
    return cart

TURN_FUNC = {
    '/': turn_on_slash,
    '\\':turn_on_backslash,
    '+': turn_on_instersection,
}

def turn(cart, tile):
    if tile in TURN_TILES:
        cart = TURN_FUNC[tile](cart)
    return cart

def move(cart, tiles, carts):
    tile = cart['tile']
    x, y = NEXT_POS[tile](cart['x'], cart['y'])
    # Check for collision
    if any((x, y) == (c['x'], c['y']) for c in carts):
        raise CollisionError(x, y, "Collision detected")
    next_tile = tiles[y][x]
    cart = turn(cart, next_tile)
    cart['x'] = x
    cart['y'] = y
    return cart

def is_cart(tile):
    return tile in CART_TILES

def process(filename):
    part1 =  part2 = None
    tiles = load_input(filename)
    tracks = tiles
    height = len(tiles)
    width = max([len(c) for c in tiles])
    carts = []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if is_cart(tile):
                cart = {
                    'x': x,
                    'y': y,
                    'tile': tile,
                    'turn': 0,
                }
                carts.append(cart)
                tracks[y][x] = TILE_UNDER_CART[tiles[y][x]]

    for tick in range(1, 20000):
        for cart in sorted(carts, key=lambda c: (c['y'],c['x'])):
            try:
                cart = move(cart, tiles, carts)
            except CollisionError as err:
                print(f'Collision at {err.x},{err.y} on tick {tick}')
                if not part1:
                    part1 = ','.join([str(err.x), str(err.y)])
                carts.remove(cart)
                carts.remove([c for c in carts if (c['x'],c['y'])==(err.x, err.y)][0])
                print(f'{len(carts)} carts left')
        if len(carts) == 1:
            last_cart = carts[0]
            part2 = ','.join([str(last_cart['x']), str(last_cart['y'])])
            break

    return (part1, part2)

if __name__ == '__main__':
    print(process('test.txt'))
    print(process('test2.txt'))
    print(process('test3.txt'))
    print(process('input'))
