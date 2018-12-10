#!/usr/bin/env python

def load_input(input_file):
    with open(input_file, 'r') as fp:
        candidates = [line for line in fp.read().splitlines()]
    return candidates

def are_close_enough(id1, id2):
    res = []
    diffs = 0
    zap = zip(id1, id2)
    for i, j in zap:
        if i == j:
            res.append(i)
        else:
            diffs += 1
    if diffs == 1:
        return ''.join(res)
    return None


def find_box(boxes):
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            res = are_close_enough(boxes[i], boxes[j])
            if res is not None:
                return res


def find_candidates(boxes):
    nb_doubles = 0
    nb_triples = 0
    candidates = []
    for box in boxes:
        c = [(box.count(i), i) for i in set(box)]
        if [i for i in c if 2 in i]:
            candidates.append(box)
            nb_doubles += 1
        if [i for i in c if 3 in i]:
            candidates.append(box)
            nb_triples += 1

    checksum = nb_doubles * nb_triples
    return (candidates, checksum)


def process(boxes):
    candidates, checksum = find_candidates(boxes)

    print('Result for part one is {}.'.format(checksum))
    print('Result for part two is {}.'.format(find_box(boxes)))

if __name__ == "__main__":
    process(load_input('input'))
