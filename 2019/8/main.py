import util
from collections import Counter


def decode_image(data, dim):
    digits = [d for d in data]
    chunk_size = dim[0] * dim[1]
    nb_layers = len(digits)//(chunk_size)
    return [[layer for layer in
            digits[c*chunk_size:(c+1)*chunk_size]]
            for c in range(nb_layers)]

def solve_part1(data, dim):
    layers = decode_image(data, dim)
    lf = [Counter(l) for l in layers]
    candidate=min(lf, key=lambda x:x.get('0'))
    return (candidate.get('1')*candidate.get('2'))

def solve_part2(data, dim):
    layers = decode_image(data, dim)
    res = layers[0]
    f = lambda f,b: b if f=='2' else f
    for l in range(1, len(layers)):
        lc = layers[l]
        res = [f(a, b) for a,b in zip(res, lc)]

    group = lambda flat, size: [flat[i:i+size] for i in range(0,len(flat), size)]
    for row in group(res, 25):
        print(''.join(row).replace('0',' ').replace('1','#'))

def solve(Part2=False):
    data = util.load_data()[0]
    if not Part2:
        print(f'Part1 = {solve_part1(data,[25, 6])}')
    else:
        print(f'Part2 = {solve_part2(data,[25, 6])}')

if __name__ == '__main__':
    solve()
    solve(Part2=True)
