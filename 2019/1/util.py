from urllib import request

def get_input(day):
    '''Gets puzzle input for given day'''
    url = f'https://adventofcode.com/2019/day/{day}/input'
    print(url)
    request.urlretrieve(url, 'input.txt')

def load_data(formater=None):
    res = []
    with open('input') as input:
        res = input.read().splitlines()
    if formater is not None:
        res = [formater(line) for line in res]
    return res
