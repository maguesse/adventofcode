import util
import intcode
from itertools import permutations


NB_PHASES = 4
NB_AMPS = 5

def amp(index, first, second, prg):
    insts = [second, first]
    return intcode.engine(prg, insts)

def eval_ampsignal(prg, settings):
    instructions = settings[::-1]
    signal = 0
    for a in range(NB_AMPS):
        signal = amp(a, instructions.pop(), signal, prg)
    return signal


def part1(prg):
    sequences = map(list, permutations(range(5)))
    max_signal = max(((s, eval_ampsignal(prg.copy(), s)) for s in sequences),
                       key=lambda x: x[1])
    return max_signal[1]

def part2(prg):
    sequences = map(list, permutations(range(5,10)))
    # TODO: implement a solution
    return 0

def solve(part2=False):
    data = util.load_list_of_ints()
    if part2 is False:
        print(f'Part1: {part1(data)}')
    else:
        print(f'Part2: {part2(data)}')

if __name__ == '__main__':
    ex1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    ex2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
           101,5,23,23,1,24,23,23,4,23,99,0,0]
    ex3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
           1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert 43210 == part1(ex1)
    assert 54321 == part1(ex2)
    assert 65210 == part1(ex3)
    solve()
    ex4 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,
           26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    ex5 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
           -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
           53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

    assert 139629729 == part2(ex4)
    assert 18216 == part2(ex5)
    solve(part2=True)

