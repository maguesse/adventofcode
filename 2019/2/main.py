import util


def engine(prg, head=0):
    opcode=prg[head]
    while opcode != 99:
        p1, p2, p3 = prg[head+1:head+4]
        if opcode == 1:
            prg[p3] = prg[p1] + prg[p2]
        elif opcode == 2:
            prg[p3] = prg[p1] * prg[p2]
        head += 4
        opcode=prg[head]

    return prg

def solve():
    data = util.load_list_of_ints()
    data[1]=12
    data[2]=2
    res = engine(data)
    print(res[0])


if __name__ == '__main__':
    print(engine([1,9,10,3,2,3,11,0,99,30,40,50]))
    print(engine([1,0,0,0,99]))
    print(engine([2,3,0,3,99]))
    print(engine([2,4,4,5,99,0]))
    print(engine([1,1,1,4,99,5,6,0,99]))
    solve()
