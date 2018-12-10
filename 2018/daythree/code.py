#!/usr/bin/env python
'''
Advent of code - Day 3
'''

import re


class Claim:
    claim_pattern = re.compile('^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')

    def __init__(self, claim_desc):
        match = Claim.claim_pattern.match(claim_desc)
        self.id, left_margin, top_margin, width, height = match.groups()
        self.x1 = int(left_margin)
        self.x2 = int(width) + self.x1
        self.y1 = int(top_margin)
        self.y2 = int(height) + self.y1


    def __repr__(self):
        return '<Claim ID:{}, x1:{}, x2:{}, y1:{}, y2:{}>'.format(self.id,
                                                                  self.x1,
                                                                  self.x2,
                                                                  self.y1,
                                                                  self.y2)

def _load_input(input_file):
    with open(input_file, 'r') as fp:
        return fp.read().splitlines()

def _process(claims_desc):
    fabric_size=1000
    fabric = [[list() for i in range(fabric_size)]
              for j in range(fabric_size)]
    claims = [Claim(desc) for desc in claims_desc]

    overlaps = 0

    for claim in claims:
        for i in range(claim.x1, claim.x2):
            for j in range(claim.y1, claim.y2):
                fabric[i][j].append(claim.id)

    for line in fabric:
        for cell in line:
            if len(cell) > 1:
                overlaps += 1

    print('Result for part one is {}.'.format(overlaps))
    print('Result for part two is {}.'.format('<TODO>'))

if __name__ == "__main__":
    _process(_load_input('input'))
