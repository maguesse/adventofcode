import util
import intcode
from itertools import permutations


NB_PHASES = 4
NB_AMPS = 5

class Amplifier:
    def __init__(self, prg, phase, id=-1):
        from string import ascii_uppercase
        self._input_signal = [phase]
        self._output_signal = 0
        self._id = ascii_uppercase[id]
        self.phase = phase
        self.ic = intcode.IntCode(prg, self.id)
        self.done = False

    @property
    def id(self):
        return self._id

    @property
    def output_signal(self):
        return self._output_signal

    @output_signal.setter
    def output_signal(self, output_signal):
        self._output_signal = output_signal

    @property
    def input_signal(self):
        return self._input_signal

    @input_signal.setter
    def input_signal(self, input_signal):
        self._input_signal.append(input_signal)


    def run(self):
        if not self.ic.is_halted:
            # Popall input before calling IC
            signal, self._input_signal = self._input_signal, []
            self.ic.run(signal)
            self.output_signal = self.ic.last_output
        else:
            self.done = True

    def __repr__(self):
        return f'<{self.__class__.__name__} #{self.id} on phase {self.phase}' \
            f', input_signal={self._input_signal}' \
            f', output_signal={self._output_signal}, done={self.done}>'


    def __str__(self):
        return f'<{self.__class__.__name__} #{self.id} on phase {self.phase}' \
            f', input_signal={self._input_signal}' \
            f', output_signal={self._output_signal}, done={self.done}>'

def eval_ampsignal(prg, settings, feedback=False):
    amps = []
    for i, phase in enumerate(settings):
        amps.append(Amplifier(prg, phase, id=i))

    if feedback == False:
        prev_signal = 0
        for amp in amps:
            amp.input_signal = prev_signal
            amp.run()
            prev_signal = amp.output_signal
    else:
        running = True
        prev_signal = 0
        while running:
            for amp in amps:
                amp.input_signal = prev_signal
                amp.run()
                prev_signal = amp.output_signal
                if amp.done:
                    # Stop when at least one amplifier as halted
                    running = False
    return prev_signal


def solve_part1(prg):
    sequences = map(list, permutations(range(NB_AMPS)))
    max_signal = max(((s, eval_ampsignal(prg.copy(), s)) for s in sequences),
                       key=lambda x: x[1])
    return max_signal

def solve_part2(prg):
    sequences = map(list, permutations(range(NB_AMPS,NB_AMPS*2)))
    max_signal = max(((s, eval_ampsignal(prg.copy(), s, feedback=True))
                      for s in sequences),
                       key=lambda x: x[1])
    return max_signal

def solve(part2=False):
    data = util.load_list_of_ints()
    if part2 is False:
        print(f'Part1: {solve_part1(data)}')
    else:
        print(f'Part2: {solve_part2(data)}')

if __name__ == '__main__':
    ex1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    ex2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
           101,5,23,23,1,24,23,23,4,23,99,0,0]
    ex3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
           1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert ([4,3,2,1,0], 43210) == solve_part1(ex1)
    assert ([0,1,2,3,4], 54321) == solve_part1(ex2)
    assert ([1,0,4,3,2], 65210) == solve_part1(ex3)
    solve()
    ex4 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,
           26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    ex5 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
           -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
           53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

    assert ([9,8,7,6,5], 139629729) == solve_part2(ex4)
    assert ([9,7,8,5,6], 18216) == solve_part2(ex5)
    solve(part2=True)

