from intcode import IntCode

def test_equals_posmode():
    prg = [3,9,8,9,10,9,4,9,99,-1,8]
    assert 1 == IntCode(prg, cpu_id='5.1.1').run([8])
    assert 0 == IntCode(prg, cpu_id='5.1.2').run([5])

def test_less_than_posmode():
    prg = [3,9,7,9,10,9,4,9,99,-1,8]
    assert 0 == IntCode(prg, cpu_id='5.2.1').run([8])
    assert 1 == IntCode(prg, cpu_id='5.2.2').run([5])

def test_equals_immediate():
    prg = [3,3,1108,-1,8,3,4,3,99]
    assert 1 == IntCode(prg, cpu_id='5.3.1').run([8])
    assert 0 == IntCode(prg, cpu_id='5.3.2').run([5])

def test_less_than_immediate():
    prg = [3,3,1107,-1,8,3,4,3,99]
    assert 0 == IntCode(prg, cpu_id='5.4.1').run([8])
    assert 1 == IntCode(prg, cpu_id='5.4.2').run([5])

def test_zero_position():
    prg = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    assert 0 == IntCode(prg, cpu_id='5.5.1').run([0])
    assert 1 == IntCode(prg, cpu_id='5.5.1').run([1])

def test_zero_immediate():
    prg = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    assert 0 == IntCode(prg, cpu_id='5.6.1').run([0])
    assert 1 == IntCode(prg, cpu_id='5.6.2').run([1])

def test_compare_to():
    prg = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    assert 999 == IntCode(prg, cpu_id='5.7.1').run([7])
    assert 1000 == IntCode(prg, cpu_id='5.7.2').run([8])
    assert 1001 == IntCode(prg, cpu_id='5.7.3').run([9])
