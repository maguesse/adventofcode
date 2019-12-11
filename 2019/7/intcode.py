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
        if DEBUG:
            print(f'DEBUG fn:{fn.__name__}, args:{args}, kargs={kargs}')
            return fn(*args, **kargs)
        return fn(*args, **kargs)

    return wrapper

class IntCode:

    def __init__(self, prg):
        self.pc = 0
        self.input = deque()
        self.output = deque()
        self.last_output = -1
        self.is_running = True
        self.is_waiting = False
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
        #if mode[0] == AccesMode.WRITE:
        #    return self.value_fetchers[AddressingMode.POSITION]
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
        self.prg[addr] = self.input.popleft()
        self.inc()

    @debug_fun
    def op_output(self, operands):
        v = operands.pop()
        self.output.append(v)
        self.last_output = self.output[-1]
        self.inc()

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

    def run(self, input):
        self.input = deque(input)
        while self.is_running:
            self.flags['jmp'] = False
            # Get OpCode and addressing modes
            opcode, *addressing_modes=IntCode.decode_opcode(self.prg[self.pc])
            # Get operation and its operands access modes
            op, *opmodes = self.instructions[opcode]
            if DEBUG: print(f'DEBUG pc:{self.pc}, prg:{self.prg}')
            if DEBUG: print(f'DEBUG opcode: {opcode}, op:{op.__name__}')
            if DEBUG: print(f'DEBUG opcode:{opmodes}, addressing_modes:{addressing_modes}')
            # Associate each operand acces mode with its addressing mode
            modes = list(zip_longest(opmodes, addressing_modes,
                                     fillvalue=AddressingMode.POSITION))
            if DEBUG: print(f'DEBUG mode:{modes}')
            op(self.fetch_values(modes))
        return self.last_output


if __name__ == '__main__':
     # Day 2
    IntCode([1,9,10,3,2,3,11,0,99,30,40,50]).run([])
    IntCode([1,0,0,0,99]).run([])
    IntCode([2,3,0,3,99]).run([])
    IntCode([2,4,4,5,99,0]).run([])
    IntCode([1,1,1,4,99,5,6,0,99]).run([])

    # Day 5 tests
    # Equals 8 ?
    assert 1 == IntCode([3,9,8,9,10,9,4,9,99,-1,8]).run([8])
    assert 0 == IntCode([3,9,8,9,10,9,4,9,99,-1,8]).run([5])

    # Less than 8 ?
    assert 0 == IntCode([3,9,7,9,10,9,4,9,99,-1,8]).run([8])
    assert 1 == IntCode([3,9,7,9,10,9,4,9,99,-1,8]).run([5])

    # Equals 8 ?
    assert 1 == IntCode([3,3,1108,-1,8,3,4,3,99]).run([8])
    assert 0 == IntCode([3,3,1108,-1,8,3,4,3,99]).run([5])

    # Less than 8 ?
    assert 0 == IntCode([3,3,1107,-1,8,3,4,3,99]).run([8])
    assert 1 == IntCode([3,3,1107,-1,8,3,4,3,99]).run([5])

    # Zero ?
    assert 0 == IntCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run([0])
    assert 1 == IntCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run([1])

    # Zero ?
    assert 0 == IntCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run([0])
    assert 1 == IntCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run([1])

    # Compare to 8
    assert 999 == IntCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).run([7])
    assert 1000 == IntCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).run([8])
    assert 1001 == IntCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).run([9])
