#!/usr/bin/env python
from collections import deque
import re
from itertools import groupby

def load_input(input_file):
    with open(input_file, 'r') as fp:
        polymers = [line for line in fp.read().splitlines()]
    return polymers

def react(polymer):
    dq_poly = deque(polymer)
    reacted = list()
    while dq_poly:
        if not reacted:
            reacted.append(dq_poly.popleft())
        buf = dq_poly.popleft()
        if abs(ord(buf) - ord(reacted[-1])) == 32:
            reacted.pop()
        else:
            reacted.append(buf)
    return reacted

def reduce(polymer):
    res = []
    for k,_ in groupby(sorted(polymer, key=lambda x: x.upper()), lambda x:
                       x.upper()):
        cleaned_poly = [c for c in polymer if c.upper() != k]
        res.append(''.join(react(cleaned_poly)))
    return res

def process(raw_polymer):
    polymer_p1 = react(raw_polymer)
    polymers_p2 = reduce(polymer_p1)

    p2_min_lenght, p2_min_polymer = min([(len(p),p) for p in polymers_p2])

    p1 = len(polymer_p1)
    p2 = p2_min_lenght
    print('Result for part one is {}.'.format(p1))
    print('Result for part two is {}.'.format(p2))

if __name__ == "__main__":
    process(load_input('input')[0])
