import util
from intcode import IntCode

def solve_part1(data):
    ic = IntCode(data, cpu_id='BOOST')
    ic.run([1])
    return ic.last_output

def solve_part2(data):
    ic = IntCode(data, cpu_id='BOOST')
    ic.run([2])
    return ic.last_output

def solve(Part2=False):
    data = util.load_list_of_ints()
    if not Part2:
        res = solve_part1(data)
    else:
        res = solve_part2(data)

    print(f'Part {2 if Part2 else 1}: {res}')

if __name__ == '__main__':
    solve()
    solve(Part2=True)
