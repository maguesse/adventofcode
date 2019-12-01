#!/usr/bin/env python
from enum import Enum, auto


class Team(Enum):
    GOBELIN = auto()
    ELF = auto()

class Unit:
    def __init__(self, pos, team):
        self.pos = pos
        self.team = team
        self.attack_power = 3
        self.hit_point = 200
        self.alive = True


    def __repr__(self):
        return (f'Unit(pos={self.pos}, team={self.team})')

    def __str__(self):
        return (f'<Unit position:{self.pos}, team:{self.team}'
                f', Power:{self.attack_power}'
                f', HP:{self.hit_point}, is alive:{self.alive}>')

class Area:
    def __init__(self, lines):

        self.units=[]

        for y, line in enumerate(lines):
            for x, cell in enumerate(line):
                if cell in 'GE':
                    self.units.append(Unit(
                        pos=(x, y),
                        team={'E':Team.ELF, 'G':Team.GOBELIN}[cell]))

    def move(self):
        pass

    def attack(self):
        pass


    def __repr__(self):
        return f'Area(units={self.units})'

def load_input(filename):
    with open(filename, 'r') as ifp:
        lines = ifp.read().splitlines()
    return [list(line) for line in lines]


def process(area):
    part1 = part2 = None

    area_map = Area(load_input(area))

    print(area_map)

    print(f'Part1:{part1}, Part2:{part2}')


if __name__ == '__main__':
    process('input')
