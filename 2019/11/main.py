import util
from enum import Enum, auto
from intcode import IntCode
from collections import defaultdict


TURN_RIGHT = {
    ( 0, -1): ( 1,  0),
    ( 1,  0): ( 0,  1),
    ( 0,  1): (-1,  0),
    (-1,  0): ( 0, -1),
}
TURN_LEFT = {
    ( 0, -1): (-1,  0),
    (-1,  0): ( 0,  1),
    ( 0,  1): ( 1,  0),
    ( 1,  0): ( 0, -1),
}
TURN = {
    0: TURN_LEFT,
    1: TURN_RIGHT,
}

class Robot:
    def __init__(self, data):
        self.position = (0,0)
        self.direction = (0, -1)
        self.cpu = IntCode(data.copy(), cpu_id = 'Robot')
        self.done = False
        self.panels = defaultdict(int)

    @property
    def min(self):
        xmin = min(self.panels, key=lambda x:x[0])[0]
        ymin = min(self.panels, key=lambda x:x[1])[1]
        return (xmin,ymin)

    @property
    def max(self):
        xmax = max(self.panels, key=lambda x:x[0])[0]
        ymax = max(self.panels, key=lambda x:x[1])[1]
        return (xmax,ymax)

    def fetch_color(self):
        return self.panels[self.position]

    def turn(self, direction):
        self.direction = TURN[direction][self.direction]

    def forward(self):
        self.position = (self.position[0] + self.direction[0]
                         , self.position[1] + self.direction[1])

    def paint(self, color):
        self.panels[self.position] = color

    def run(self):
        if self.done:
            return
        while not self.cpu.is_halted:
            col = self.fetch_color()
            self.cpu.run([col])
            self.paint(self.cpu.output.popleft())
            self.turn(self.cpu.output.popleft())
            self.forward()

class Puzzle:
    def __init__(self, data):
        self.prg = data

    def solve_part1(self):
        self.robot = Robot(self.prg.copy())
        self.robot.run()
        return(len(self.robot.panels))

    def solve_part2(self):
        self.robot = Robot(self.prg.copy())
        self.robot.panels[(0,0)] = 1
        self.robot.run()

        xmin,ymin = self.robot.min
        xmax, ymax = self.robot.max
        res = []
        for y in range(ymin,ymax+1):
            row = []
            for x in range(xmin,xmax+1):
                row.append('#' if self.robot.panels[(x,y)] else ' ')
            res.append(''.join(row))
        return '\n'.join(res)

if __name__ == '__main__':
    puzzle = Puzzle(util.load_list_of_ints())
    print(f'Part 1: {puzzle.solve_part1()}')
    print(f'Part 2: \n{puzzle.solve_part2()}')
