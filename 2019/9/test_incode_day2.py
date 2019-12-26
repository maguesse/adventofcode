from intcode import IntCode


def test_1():
    IntCode([1,9,10,3,2,3,11,0,99,30,40,50], cpu_id='2.1').run([])
def test_2():
    IntCode([1,0,0,0,99], cpu_id='2.2').run([])
def test_3():
    IntCode([2,3,0,3,99], cpu_id='2.3').run([])
def test_4():
    IntCode([2,4,4,5,99,0], cpu_id='2.4').run([])
def test_5():
    IntCode([1,1,1,4,99,5,6,0,99], cpu_id='2.5').run([])

