#!/usr/bin/env python
import re
from collections import deque


def load_input(filename):
    initptn = re.compile('initial state: (.*)')
    ruleptn = re.compile('(.{5}) => (.)')
    with open(filename, 'r') as ifp:
        lines = ifp.read().splitlines()
    m = initptn.match(lines[0])
    if m is None:
        raise ValueError('Unable to read input')
    initial_state = m.group(1)
    rules = {}
    for r in lines[2:]:
        m = ruleptn.match(r)
        if m is None:
            raise ValueError('Unable to read input')
        rules[m.group(1)] = m.group(2)
    return (initial_state, rules)

def next_gen(current_state, rules):
    new_state = ''
    for x in range(2, len(current_state)-2):
        window = current_state[x-2:x+3]
        new_state += rules.get(window, '.')
    return new_state

def sum_plan(state, init_len):
    index_offset = (len(state) - init_len)//2
    return sum([i - index_offset for i,p in enumerate(state) if p == '#'])

def process(filename):
    state, rules = load_input(filename)
    padding = '...'
    init_len = len(state)
    prev_sum = sum_plan(state, init_len)
    part1 = None
    part2 = None
    deltas = deque([], 5)
    for gen in range(2000):
        if gen == 20:
            part1 = prev_sum
        state = padding + state + padding
        state = next_gen(state, rules)
        cur_sum = sum_plan(state, init_len)
        delta = cur_sum - prev_sum
        deltas.append(delta)
        if len(deltas)> 2 and (len(set(deltas))<=1):
            # When the nth last deltas are the same, we entered a linear mode
            break
        prev_sum = cur_sum
    part2 = (50_000_000_000 - (gen+1)) * delta + cur_sum
    return (part1, part2)

if __name__ == '__main__':
    print(process('input'))
