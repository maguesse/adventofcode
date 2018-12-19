#!/usr/bin/env python
import re
from itertools import groupby
from collections import defaultdict, deque


def process_part1(instructions):
    result = list()
    steps = set([i[0] for i in instructions] +
                [i[1] for i in instructions])
    edges = defaultdict(list)
    in_depth = defaultdict(int)
    for src, dest in instructions:
        edges[src].append(dest)
        in_depth[dest] += 1
    for src in edges:
        edges[src] = sorted(edges[src])

    roots = deque([s for s in steps if in_depth[s] == 0])
    while roots:
        c = roots.popleft()
        result.append(c)
        for dest in edges[c]:
            in_depth[dest] -= 1
            if in_depth[dest] == 0:
                roots.append(dest)
        roots = deque(sorted(roots))

    return ''.join(result)


def end_time(step, start_time, offset):
    return start_time + offset + 1 + ord(step) - ord('A')


def do_work(start_time, nb_workers, offset,
            available_tasks, working_queue):
    while len(working_queue) < nb_workers and available_tasks:
        current_task = available_tasks.popleft()
        working_queue.append((end_time(current_task, start_time, offset)
                              , current_task))
    return available_tasks, deque(sorted(working_queue))


def plan_work(nb_workers, offset, edges, in_depth):
    available_tasks, working_queue = do_work(0, nb_workers, offset,
                                             deque([t for t in edges if
                                                    in_depth[t] == 0]),
                                             deque([]))
    while working_queue or available_tasks:
        time, task = working_queue.popleft()
        for dest in edges[task]:
            in_depth[dest] -= 1
            if in_depth[dest] == 0:
                available_tasks.append(dest)
        available_tasks, working_queue = do_work(time, nb_workers, offset,
                                                 available_tasks,
                                                 working_queue)

    return time



def process_part2(instructions, nb_workers=5, offset=60):
    edges = defaultdict(list)
    in_depth = defaultdict(int)
    for src, dest in instructions:
        edges[src].append(dest)
        in_depth[dest] += 1
    for src in edges:
        edges[src] = sorted(edges[src])
    return plan_work(nb_workers, offset, edges, in_depth)

def load_input(filename):
    ptn = re.compile(' ([A-Z]) ')
    return list(tuple(ptn.findall(line))
                for line in open(filename, 'r'))

if __name__=='__main__':
    assert ('CABDFE', 15) == (process_part1(load_input('test.txt')),
                                process_part2(load_input('test.txt'),
                                              nb_workers=2, offset=0))
    print('\n' + '*'*80 +'\n')
    print(process_part1(load_input('input')),
          process_part2(load_input('input')))
