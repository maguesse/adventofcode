from itertools import zip_longest


IP_OFFSET = {
    1:4, # ADD
    2:4, # MUL
    3:2, # IN
    4:2, # OUT
    5:3, # JMP_IF_TRUE
    6:3, # JMP_IF_FALSE
    7:4, # LESS THAN
    8:4, # EQUALS
}

OPERATORS = {
    1:lambda x,y: x + y,
    2:lambda x,y: x * y,
    5:lambda x,y: x != 0,
    6:lambda x,y: x == 0,
    7:lambda x,y: 1 if x < y else 0,
    8:lambda x,y: 1 if x == y else 0,
}

def decode_opcode(opcode):
    if opcode <= 99:
        return ([opcode, 0, 0])
    _s=str(opcode)
    # _s[-2:] gets 2 rightmost digits
    # _s[:-2][::-1] gets leftmost digits and reverse them
    return ([int(_s[-2:])] + list(map(int,list(_s[:-2][::-1]))))

def get_values(prg, insts):
    res = []
    for inst in insts:
        if inst[1] == 0:
            res.append(prg[inst[0]])
        else:
            res.append(inst[0])

    return res

def engine(prg, inqueue, outqueue=[]):
    pc = 0
    output = []
    while True:
        opcode, *modes=decode_opcode(prg[pc])
        if opcode in OPERATORS.keys():
            ops = list(zip_longest(prg[pc+1:pc+3], modes, fillvalue=0))
            val1, val2 = get_values(prg, ops)
            res = OPERATORS[opcode](val1, val2)
            if (opcode <5) | (opcode > 6) :
                prg[prg[pc+3]] = res
                pc += IP_OFFSET[opcode]
            else:
                if res:
                    pc = val2
                else:
                    pc += IP_OFFSET[opcode]
        elif opcode == 3:
            value = inqueue.pop()
            prg[prg[pc+1]] = value
            pc += IP_OFFSET[opcode]
        elif opcode == 4:
            output.append(prg[prg[pc+1]])
            pc += IP_OFFSET[opcode]
        elif opcode == 99:
            break
    return output[0]

