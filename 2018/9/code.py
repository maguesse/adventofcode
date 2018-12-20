#!/usr/bin/env python
import re
from itertools import cycle
from collections import deque


def process(data, factor=1):
    nb_players, worth = data

    marbles = [i for i in range(factor*(worth+1))]
    marbles = sorted(marbles, reverse=True)
    circle = deque([])
    players_marbles = [[] for _ in range(nb_players)]
    for player in cycle(range(nb_players)):
        try:
            marble = marbles.pop()
            if marble >0 and marble % 23 == 0:
                circle.rotate(7)
                players_marbles[player].append(marble)
                players_marbles[player].append(circle.pop())
                circle.rotate(-1)
            else:
                circle.rotate(-1)
                circle.append(marble)
        except IndexError:
            break

    players_scores = [sum(p) for p in players_marbles]
    return(max(players_scores))

def load_input(filename):
    marble_ptn = re.compile('(\d+)')
    return list(tuple([int(s) for s in marble_ptn.findall(line)])
                for line in open(filename, 'r').read().splitlines())

if __name__=='__main__':
    for d in load_input('test.txt'):
        expect = d[-1]
        res = process(d[:2])
        assert res == expect, f'Expected : {expect}, got : {res}'

    #Part 1
    for d in load_input('input'):
        print(process(d))

    #Part 2
    for d in load_input('input'):
        print(process(d, factor=100))
