from enum import IntEnum
import functools
from itertools import zip_longest
from queue import deque

DEBUG = False

class AccesMode(IntEnum):
    READ = 0
    WRITE = 1

class AddressingMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

def debug_fun(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kargs):
        #if DEBUG:
        #    print(f'DEBUG fn:{fn.__name__}, args:{args}, kargs={kargs}')
        #    return fn(*args, **kargs)
        return fn(*args, **kargs)

    return wrapper

class IntCode:

    def __init__(self, prg, cpu_id=-1):
        self.pc = 0
        self.input = deque()
        self.output = deque()
        self.last_output = -1
        self.is_running = True
        self.is_waiting = False
        self.is_halted = False
        self.cpu_id = cpu_id
        self.prg = prg.copy()
        self.instructions = {
            1:(self.op_add, AccesMode.READ, AccesMode.READ, AccesMode.WRITE),
            2:(self.op_mul, AccesMode.READ, AccesMode.READ, AccesMode.WRITE),
            3:(self.op_input, AccesMode.WRITE, ),
            4:(self.op_output, AccesMode.READ,),
            5:(self.op_jmp_not_zero, AccesMode.READ, AccesMode.READ),
            6:(self.op_jmp_zero, AccesMode.READ, AccesMode.READ),
            7:(self.op_less_than, AccesMode.READ, AccesMode.READ, AccesMode.WRITE),
            8:(self.op_equals, AccesMode.READ, AccesMode.READ, AccesMode.WRITE),
            99:(self.op_halt,),
        }
        self.value_fetchers = {
            AddressingMode.POSITION:self.position_fetcher,
            AddressingMode.IMMEDIATE:self.immediate_fetcher,
        }
        self.flags = {
            'jmp':False
        }

    def __repr__(self):
        return f'<{self.__class__.__name__} #{self.cpu_id} with input {list(self.input)}'\
            f' and output {list(self.output)}' \
            f' is {"not " if not self.is_running else ""}running' \
            f', is {"not " if not self.is_halted else ""}halted'\
            f', is {"not " if not self.is_waiting else ""}waiting' \
            f', last output was {self.last_output}' \
            f', pc is {self.pc}'\
            f', prg is {self.prg}>'

    @staticmethod
    @debug_fun
    def decode_opcode(opcode):
        if opcode <= 99:
            return ([opcode, ])
        _s=str(opcode)
        # _s[-2:] gets 2 rightmost digits
        # _s[:-2][::-1] gets leftmost digits and reverse them
        return ([int(_s[-2:])] + list(map(lambda i:
                                          AddressingMode(int(i)),
                                          list(_s[:-2][::-1]))))

    @debug_fun
    def position_fetcher(self, addr):
        return self.prg[addr]

    @debug_fun
    def immediate_fetcher(self, val):
        return val

    @debug_fun
    def fn_fetch_value(self, mode):
        return self.value_fetchers[mode[0] + mode[1]]

    @debug_fun
    def fetch_values(self, modes):
        res = []
        for mode in modes:
            res.append(self.fn_fetch_value(mode)(self.prg[self.pc + 1]))
            self.inc()
        return res

    @debug_fun
    def inc(self, i=1):
        self.pc += i

    @debug_fun
    def jmp(self, addr):
        self.pc = addr

    @debug_fun
    def op_add(self, operands):
        v1, v2, addr = operands
        self.prg[addr] = v1 + v2
        self.inc()

    @debug_fun
    def op_mul(self, operands):
        v1, v2, addr = operands
        self.prg[addr] = v1 * v2
        self.inc()

    @debug_fun
    def op_input(self, operands):
        addr = operands.pop()
        if len(self.input) == 0:
            self.is_waiting = True
            self.inc(-1)
            return
        self.prg[addr] = self.input.popleft()
        self.inc()

    @debug_fun
    def op_output(self, operands):
        v = operands.pop()
        self.output.append(v)
        self.last_output = self.output[-1]
        self.inc()
        self.is_waiting = True

    @debug_fun
    def op_jmp_not_zero(self, operands):
        v1, addr = operands
        if v1 != 0:
            self.jmp(addr)
        else:
            self.inc()

    @debug_fun
    def op_jmp_zero(self, operands):
        v1, addr = operands
        if v1 == 0:
            self.jmp(addr)
        else:
            self.inc()

    @debug_fun
    def op_less_than(self, operands):
        v1, v2, addr = operands
        self.prg[addr] = 1 if v1 < v2 else 0
        self.inc()

    @debug_fun
    def op_equals(self, operands):
        v1, v2, addr = operands
        self.prg[addr] = 1 if v1 == v2 else 0
        self.inc()

    @debug_fun
    def op_halt(self, _):
        self.is_running = False
        self.is_halted = True

    def run(self, input):
        self.input = deque(input)
        if self.is_halted:
            print("IntCode computer is halted.")
            return
        self.is_waiting = False
        if DEBUG: print(f'Running {self}')
        while self.is_running and not self.is_waiting:
            self.flags['jmp'] = False
            # Get OpCode and addressing modes
            opcode, *addressing_modes=IntCode.decode_opcode(self.prg[self.pc])
            # Get operation and its operands access modes
            op, *opmodes = self.instructions[opcode]
            if DEBUG: print(80*'*')
            if DEBUG: print(f'DEBUG CPU #{self.cpu_id} pc:{self.pc}, prg:{self.prg}')
            if DEBUG: print(f'DEBUG CPU #{self.cpu_id} opcode: {opcode}, op:{op.__name__}')
            if DEBUG: print(f'DEBUG CPU #{self.cpu_id} opcode:{opmodes}, addressing_modes:{addressing_modes}')
            # Associate each operand acces mode with its addressing mode
            modes = list(zip_longest(opmodes, addressing_modes,
                                     fillvalue=AddressingMode.POSITION))
            if DEBUG: print(f'DEBUG CPU #{self.cpu_id} mode:{modes}')
            op(self.fetch_values(modes))
            if DEBUG: print(f'State {self}')
        return self.last_output


if __name__ == '__main__':
    # Day 2
    test='Day 2 - Test 1'
    IntCode([1,9,10,3,2,3,11,0,99,30,40,50]).run([])
    print(f'{test} OK')
    test='Day 2 - Test 2'
    IntCode([1,0,0,0,99]).run([])
    print(f'{test} OK')
    test='Day 2 - Test 3'
    IntCode([2,3,0,3,99]).run([])
    print(f'{test} OK')
    test='Day 2 - Test 4'
    IntCode([2,4,4,5,99,0]).run([])
    print(f'{test} OK')
    test='Day 2 - Test 5'
    IntCode([1,1,1,4,99,5,6,0,99]).run([])
    print(f'{test} OK')

    # Day 5 tests
    # Equals 8 ?
    test='Day 5 - Test 1.1 - Input equals 8? (Position mode)'
    assert 1 == IntCode([3,9,8,9,10,9,4,9,99,-1,8]).run([8]), f'{test} KO'
    print(f'{test} OK')
    test='Day 5 - Test 1.2 - Input equals 8? (Position mode)'
    assert 0 == IntCode([3,9,8,9,10,9,4,9,99,-1,8]).run([5]), f'{test} KO'
    print(f'{test} OK')

    # Less than 8 ?
    test='Day 5 - Test 2.1 - Input less than 8? (Position mode)'
    assert 0 == IntCode([3,9,7,9,10,9,4,9,99,-1,8]).run([8]), f'{test} KO'
    print(f'{test} OK')
    test='Day 5 - Test 2.2 - Input less than 8? (Position mode)'
    assert 1 == IntCode([3,9,7,9,10,9,4,9,99,-1,8]).run([5]), f'{test} KO'
    print(f'{test} OK')

    # Equals 8 ?
    test='Day 5 - Test 3.1 - Input equals 8? (Immediate mode)'
    assert 1 == IntCode([3,3,1108,-1,8,3,4,3,99]).run([8]), f'{test} KO'
    print(f'{test} OK')
    test='Day 5 - Test 3.2 - Input equals 8? (Immediate mode)'
    assert 0 == IntCode([3,3,1108,-1,8,3,4,3,99]).run([5]), f'{test} KO'
    print(f'{test} OK')

    # Less than 8 ?
    test='Day 5 - Test 4.1 - Input less than 8? (Immediate mode)'
    assert 0 == IntCode([3,3,1107,-1,8,3,4,3,99]).run([8]), f'{test} KO'
    print(f'{test} OK')
    test='Day 5 - Test 4.2 - Input less than 8? (Immediate mode)'
    assert 1 == IntCode([3,3,1107,-1,8,3,4,3,99]).run([5]), f'{test} KO'
    print(f'{test} OK')

    # Zero ?
    test='Day 5 - Test 5.1 - Input is 0? (Position mode)'
    assert 0 == IntCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run([0]), f'{test} KO'
    print(f'{test} OK')
    test='Day 5 - Test 5.2 - Input is 0? (Position mode)'
    assert 1 == IntCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run([1]), f'{test} KO'
    print(f'{test} OK')

    # Zero ?
    test='Day 5 - Test 6.1 - Input is 0? (Immediate mode)'
    assert 0 == IntCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run([0]), f'{test} KO'
    print(f'{test} OK')
    test='Day 5 - Test 6.2 - Input is 0? (Immediate mode)'
    assert 1 == IntCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run([1]), f'{test} KO'
    print(f'{test} OK')

    # Compare to 8
    test='Day 5 - Test 7.1 - Compare to 8'
    assert 999 == IntCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).run([7]), f'{test} KO'
    print(f'{test} OK')
    test='Day 5 - Test 7.2 - Compare to 8'
    assert 1000 == IntCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).run([8]), f'{test} KO'
    print(f'{test} OK')
    test='Day 5 - Test 7.3 - Compare to 8'
    assert 1001 == IntCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).run([9]), f'{test} KO'
    print(f'{test} OK')

    # Amplifier
    test='Day 7 - Test 1.1 - Amplifier Feedback'
    assert 5 == IntCode([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                         27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]).run([9, 0]), f'{test} KO'
    assert 7 == IntCode([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                         27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]).run([9, 1]), f'{test} KO'
