from enum import IntEnum
import functools
from itertools import zip_longest
from queue import deque
from collections import defaultdict

DEBUG = False
TRACE = False

def debug(*args, **kargs):
    cpu = args[0]
    print(f'[DEBUG] CPU#{cpu.cpu_id} [tick: {cpu.tick}, pc: {cpu.pc}'\
          f', sp: {cpu.sp}] {kargs}')

class AccessMode(IntEnum):
    READ = 0
    WRITE = 1

class AddressingMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2
    RELATIVE2 = 3 # Very messy ack!! Only to handle relative write operation

def trace_fun(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kargs):
        if TRACE:
            print(f'TRACE fn:{fn.__name__}, args:{args}, kargs={kargs}')
            return fn(*args, **kargs)
        return fn(*args, **kargs)
    return wrapper

class IntCode:

    def __init__(self, prg, cpu_id=-1):
        self.pc = 0 # Program Counter
        self.sp = 0 # Stack Pointer
        self.input = deque()
        self.output = deque()
        self.last_output = -1
        self.is_running = True
        self.is_waiting = False
        self.is_halted = False
        self.cpu_id = cpu_id
        self.tick = 0
        ''' Computer's available memory should be much larger than the
        initial program. Memory beyond the initial program starts with the
        value 0.'''
        self.prg = defaultdict(int)
        for i, v in enumerate(prg.copy()):
            self.prg[i] = v
        self.instructions = {
            1:(self.op_add, AccessMode.READ, AccessMode.READ, AccessMode.WRITE),
            2:(self.op_mul, AccessMode.READ, AccessMode.READ, AccessMode.WRITE),
            3:(self.op_input, AccessMode.WRITE,),
            4:(self.op_output, AccessMode.READ,),
            5:(self.op_jmp_not_zero, AccessMode.READ, AccessMode.READ),
            6:(self.op_jmp_zero, AccessMode.READ, AccessMode.READ),
            7:(self.op_less_than, AccessMode.READ, AccessMode.READ, AccessMode.WRITE),
            8:(self.op_equals, AccessMode.READ, AccessMode.READ, AccessMode.WRITE),
            9:(self.op_set_offset, AccessMode.READ),
            99:(self.op_halt,),
        }
        self.value_fetchers = {
            AddressingMode.POSITION:self.position_fetcher,
            AddressingMode.IMMEDIATE:self.immediate_fetcher,
            AddressingMode.RELATIVE:self.relative_fetcher,
            AddressingMode.RELATIVE2:self.relative2_fecther,
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
            f'>'

    @staticmethod
    @trace_fun
    def decode_opcode(opcode):
        if opcode <= 99:
            return ([opcode, ])
        _s=str(opcode)
        # _s[-2:] gets 2 rightmost digits
        # _s[:-2][::-1] gets leftmost digits and reverse them
        return ([int(_s[-2:])] + list(map(lambda i:
                                          AddressingMode(int(i)),
                                          list(_s[:-2][::-1]))))

    ''' Utility functions '''
    @trace_fun
    def position_fetcher(self, addr):
        return self.prg[addr]

    @trace_fun
    def immediate_fetcher(self, val):
        return val

    @trace_fun
    def relative_fetcher(self, addr):
        return self.prg[addr + self.sp]

    @trace_fun
    def relative2_fecther(self, addr):
        return addr + self.sp

    @trace_fun
    def fn_fetch_value(self, mode):
        '''
        mode[0] : Access Mode (Read or Write)
        mode[1] : Addressing Mode (position, immediate, relative

        Write cannot be immediate
        '''
        if mode[0] == AccessMode.WRITE:
            return self.value_fetchers[mode[0] + mode[1]]
        else:
            return self.value_fetchers[mode[1]]

    @trace_fun
    def fetch_values(self, modes):
        res = []
        for mode in modes:
            res.append(self.fn_fetch_value(mode)(self.prg[self.pc + 1]))
            self.inc()
        return res

    @trace_fun
    def inc(self, i=1):
        self.pc += i

    @trace_fun
    def jmp(self, addr):
        self.pc = addr

    ''' Operation functions '''
    @trace_fun
    def op_add(self, operands):
        ''' Addition '''
        v1, v2, addr = operands
        self.prg[addr] = v1 + v2
        self.inc()

    @trace_fun
    def op_mul(self, operands):
        ''' Multiplication '''
        v1, v2, addr = operands
        self.prg[addr] = v1 * v2
        self.inc()

    @trace_fun
    def op_input(self, operands):
        ''' Read input '''
        addr = operands.pop()
        if len(self.input) == 0:
            self.is_waiting = True
            self.inc(-1)
            return
        self.prg[addr] = self.input.popleft()
        self.inc()

    @trace_fun
    def op_output(self, operands):
        ''' Write output '''
        v = operands.pop()
        self.output.append(v)
        self.last_output = self.output[-1]
        self.inc()
        ''' TODO Understand why this is required to set is_waiting state
        to True for amplifiers, but not for other cases
        '''
        #self.is_waiting = True

    @trace_fun
    def op_jmp_not_zero(self, operands):
        ''' Jump if not zero '''
        v1, addr = operands
        if v1 != 0:
            self.jmp(addr)
        else:
            self.inc()

    @trace_fun
    def op_jmp_zero(self, operands):
        ''' Jump if zero '''
        v1, addr = operands
        if v1 == 0:
            self.jmp(addr)
        else:
            self.inc()

    @trace_fun
    def op_less_than(self, operands):
        ''' Less than '''
        v1, v2, addr = operands
        self.prg[addr] = 1 if v1 < v2 else 0
        self.inc()

    @trace_fun
    def op_equals(self, operands):
        ''' Equals '''
        v1, v2, addr = operands
        self.prg[addr] = 1 if v1 == v2 else 0
        self.inc()

    @trace_fun
    def op_set_offset(self, operands):
        ''' Set relative base offset'''
        v = operands.pop()
        self.sp += v
        self.inc()

    @trace_fun
    def op_halt(self, _):
        ''' Halt '''
        self.is_running = False
        self.is_halted = True

    def run(self, input):
        self.input = deque(input)
        if self.is_halted:
            print("IntCode computer is halted.")
            return
        self.is_waiting = False
        while self.is_running and not self.is_waiting:
            self.flags['jmp'] = False
            # Get OpCode and addressing modes
            opcode, *addressing_modes=IntCode.decode_opcode(self.prg[self.pc])
            if DEBUG: debug(self, opcode=opcode, addressing_modes=addressing_modes)
            # Get operation and its operands access modes
            op, *opmodes = self.instructions[opcode]
            if DEBUG: debug(self, op=op.__name__, opmodes=opmodes)
            # Associate each operand acces mode with its addressing mode
            modes = list(zip_longest(opmodes, addressing_modes,
                                     fillvalue=AddressingMode.POSITION))
            if DEBUG: debug(self, op=op.__name__, modes=modes)
            if TRACE:
                print(f'[TRACE] CPU#{self.cpu_id} [prg: {self.prg}]')
                print(f'[TRACE] CPU#{self.cpu_id} [mode: {opmodes}'\
                      f', addressing: {addressing_modes}]')
            op(self.fetch_values(modes))
            self.tick += 1
        return self.last_output


if __name__ == '__main__':
    print("Please launch pytest")
    import pytest
    pytest.main()
