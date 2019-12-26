from intcode import IntCode

def test_selfcopy():
    prg = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    ic = IntCode(prg, cpu_id = 'SelfCopy')
    ic.run([])
    assert prg == list(ic.output)

def test_16digit():
    prg = [1102,34915192,34915192,7,4,7,99,0]
    ic = IntCode(prg, cpu_id = '16Digit')
    ic.run([])
    assert 16 == len(str(ic.last_output))


def test_middle():
    prg = [104,1125899906842624,99]
    ic = IntCode(prg, cpu_id = 'Middle')
    ic.run([])
    assert prg[1] == ic.last_output
