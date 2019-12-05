import util
from itertools import groupby


def is_valid_pwd(candidate, part2=False):
    if len(candidate) != 6:
        return False
    if candidate[-1] < candidate[0]:
        return False
    if part2:
        reps = []
        for _, g in groupby(candidate):
            reps.append(len(list(g)))
        return (2 in reps) & (list(candidate) == sorted(candidate))
    else:
        doubles = False # Two adjacent digits are the same
        increase = True # Pair of digit never decrease
        p=None
        for c in candidate:
            if p is not None:
                if increase == True:
                    increase = (c>=p)
                if doubles == False:
                    doubles = (c==p)
            p = c
        return doubles & increase

def solve(data):
    start,end = list(map(int, data.split('-')))
    valid_passwords = [i for i in range(start, end+1) if is_valid_pwd(str(i))]
    print(f'Part 1: {len(valid_passwords)}')
    valid_passwords = [i for i in valid_passwords if is_valid_pwd(str(i),
                                                                  part2=True)]
    print(f'Part 2: {len(valid_passwords)}')

if __name__ == '__main__':
    ex1 = '111111'
    ex2 = '223450'
    ex3 = '123789'
    ex4 = '112233'
    ex5 = '123444'
    ex6 = '111122'

    assert True == is_valid_pwd(ex1)
    assert False == is_valid_pwd(ex2)
    assert False == is_valid_pwd(ex3)

    assert True == is_valid_pwd(ex4, True)
    assert False == is_valid_pwd(ex5, True)
    assert True == is_valid_pwd(ex6, True)

    solve('128392-643281')
