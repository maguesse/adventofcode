import util
from itertools import groupby
from math import atan2, pi, hypot
from typing import TypeVar, Generic

T = TypeVar('T')

class Asteroid(Generic[T]):
    def __init__(self, x:int, y:int) -> None:
        self._x = x
        self._y = y
        self._los = [T]

    @property
    def xy(self) -> (int, int):
        return (self._x, self._y)

    @property
    def line_of_sight(self) -> T:
        return self._los

    def angle_with(self, other:T) -> float:
        '''
        Computes angle between current asteroid and another one
        '''
        ax, ay = self.xy
        bx, by = other.xy
        dx = bx - ax
        dy = by - ay
        return  atan2(dx, dy)

    def distance_to(self, other:T) -> int:
        '''
        Computes the distance between current asteroid and another one
        '''
        ax, ay = self.xy
        bx, by = other.xy
        dx = bx - ax
        dy = by - ay
        return hypot(dx, dy)

    def compute_line_of_sight(self, asteroids:[T]) -> {float}:
        '''
        Computes current asteroid's line of sight
        '''
        self._los = {self.angle_with(asteroid) for asteroid in asteroids
                if asteroid.xy != self.xy}

    def __lt__(self, other):
        return self.xy < other.xy

    def __repr__(self):
        return f'<Asteroid @{self.xy} with {len(self._los)}' \
            ' asteroids in line of sight>'

class MonitoringStation():
    def __init__(self, field:[str]) -> None:
        self._field = self.parse_field(field)
        self._vaporized = []

    @staticmethod
    def parse_field(data:[str]) -> [Asteroid]:
        return [Asteroid(x,y) for y, row in enumerate(data)
                for x, cell in enumerate(row)
                if cell == '#']

    @property
    def station(self) -> Asteroid:
        return self._station

    @station.setter
    def station(self, station: Asteroid) -> None:
        self._station = station

    def find_station(self) -> None:
        '''
        Find the best place to build the station
        '''
        for asteroid in self._field:
            asteroid.compute_line_of_sight(self._field)
        self.station = max([asteroid for asteroid in self._field],
                  key=lambda x: len(x.line_of_sight))
        self._field.remove(self.station)


    def vaporize_asteroids(self):
        '''
        Sort asteroids :
            - First by distance from station
            - then by reverse angle from station
        '''
        res = sorted(((asteroid.xy,
                       self.station.angle_with(asteroid),
                       self.station.distance_to(asteroid))
                      for asteroid in self._field),
                      key=lambda x: x[2])
        res = sorted(res, key=lambda x: x[1], reverse=True)
        ''' Group by angles '''
        groups = []
        keys = []
        for k, v in groupby(res, key=lambda x:x[1]):
            groups.append(list(v))
            keys.append(k)

        res = list(zip(keys, groups))
        idx = 0
        for _ in range(1,201):
            self._vaporized.append(res[idx][1].pop(0))
            idx = (idx + 1) % len(res)

class Day10:
    def __init__(self, data):
        self.ms = MonitoringStation(data)
        self.ms.find_station()

    def solve_part1(self):
        return (self.ms.station.xy, len(self.ms.station.line_of_sight))

    def solve_part2(self):
        self.ms.vaporize_asteroids()
        res = self.ms._vaporized[199]
        return 100 * res[0][0] + res[0][1]

if __name__ == '__main__':
    import pytest
    if pytest.main() == 0:
        obj = Day10(util.load_data())
        print(f'Part 1: {obj.solve_part1()}')
        print(f'Part 2: {obj.solve_part2()}')
