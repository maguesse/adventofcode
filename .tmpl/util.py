def load_data(formater=None):
    res = []
    with open('input') as input:
        res = input.read().splitlines()
    if formater is not None:
        res = [formater(line) for line in res]
    return res
