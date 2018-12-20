#!/usr/bin/env python



def parse(head, tail):
    nb_child, nb_meta = head
    sum_meta = 0
    meta=[]
    values = []
    print(f'Node nb_child:{nb_child}, nb_meta:{nb_meta}')
    for i in range(nb_child):
        sum_tmp, value, tail = parse(tail[:2], tail[2:])
        sum_meta += sum_tmp
        values.append(value)

    meta = tail[:nb_meta]
    tail = tail[nb_meta:]
    sum_meta += sum(meta)
    if nb_child == 0:
        return (sum_meta, sum(meta), tail)
    else:
        return (sum_meta,
                sum([values[m-1] for m in meta if m <= len(values)]),
                tail)
def process(data):
    sum_meta, value, _ = parse(data[:2],data[2:])
    return sum_meta, value



def load_input(filename):
    return [[int(c) for c in line.strip().split(' ')] for line in
            open(filename)][0]

if __name__=='__main__':
    assert (138, 66) == process(load_input('test.txt'))
    print('\n' + '*'*80 +'\n')
    print(process(load_input('input')))
