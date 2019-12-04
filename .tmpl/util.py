def load_data(formater=None):
    res = []
    with open('input') as input:
        res = input.read().splitlines()
    if formater is not None:
        res = [formater(line) for line in res]
    return res

def load_list_of_ints():
    res = []
    with open('input') as input:
        res = [int(i) for line in
               input.read().splitlines() for i in line.split(',')]
    return res

def load_lists_of_strings():
    data = [line.rstrip('\r\n').split(',') for line in open('input')]
    return data
