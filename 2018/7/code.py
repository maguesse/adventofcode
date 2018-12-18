#!/usr/bin/env python
import re
from itertools import groupby
from collections import defaultdict, deque


def process(instructions):
    result = list()
    steps = set([i[0] for i in instructions] +
                [i[1] for i in instructions])
    edges = defaultdict(list)
    in_depth = defaultdict(int)
    for src, dest in instructions:
        edges[src].append(dest)
        in_depth[dest] += 1
    for src in edges:
        edges[src] = sorted(edges[src])

    roots = deque([s for s in steps if in_depth[s] == 0])
    while roots:
        c = roots.popleft()
        result.append(c)
        for dest in edges[c]:
            in_depth[dest] -= 1
            if in_depth[dest] == 0:
                roots.append(dest)
        roots = deque(sorted(roots))


    p1 = ''.join(result)
    p2 = None
    return p1, p2

def load_input(filename):
    ptn = re.compile(' ([A-Z]) ')
    return list(tuple(ptn.findall(line))
                for line in open(filename, 'r'))

if __name__=='__main__':
    assert ('CABDFE', None) == process(load_input('test.txt'))
    print('\n' + '*'*80 +'\n')
    print(process(load_input('input')))
