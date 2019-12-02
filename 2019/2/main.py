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

def part1(indata):
    data = indata[:]
    data[1]=12
    data[2]=2
    res = engine(data)
    return res

def part2(indata, expected):
    for noun in range(0,100):
        for verb in range(0,100):
            data = indata[:]
            data[1]=noun
            data[2]=verb
            try:
                res = engine(data)[0]
                if res == expected:
                    return noun*100 + verb
            except IndexError:
                pass

def solve():
    data = util.load_list_of_ints()
    print(f'Part1: {part1(data)[0]}')
    print(f'Part2: {part2(data,19690720)}')


if __name__ == '__main__':
    assert [3500,9,10,70,2,3,11,0,99,30,40,50] == engine([1,9,10,3,2,3,11,0,99,30,40,50])
    assert [2,0,0,0,99] == engine([1,0,0,0,99])
    assert [2,3,0,6,99] == engine([2,3,0,3,99])
    assert [2,4,4,5,99,9801] == engine([2,4,4,5,99,0])
    assert [30,1,1,4,2,5,6,0,99] == engine([1,1,1,4,99,5,6,0,99])
    solve()
