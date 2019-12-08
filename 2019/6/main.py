import util
from collections import deque


'''
Both part 1 & part 2 solution were copied from Reddit r/adventofcode
Because after 6 straigth hours trying to find a fucking solution to this
fucking puzzle, I gave up !!!!!!!!!
Shame on me !!!!
'''


def path_length(tree, node):
    children = tree.get(node,[])
    return len(children) + sum((path_length(tree, c) for c in children))

def path(connexions, links, you='YOU',santa='SAN'):
    ''' Breadth-First 
    Freely inspired from
    https://www.reddit.com/r/adventofcode/comments/e6tyva/2019_day_6_solutions/f9w4q1z?utm_source=share&utm_medium=web2x
    '''
    start = [k for k,v in connexions.items() if you in v].pop()
    end = [k for k,v in connexions.items() if santa in v].pop()
    dists = {start:0}
    objs = deque([start])
    seen = {start}
    while end not in dists:
        n = objs.pop()
        dist = dists[n]
        for neighbor in links[n]:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            objs.appendleft(neighbor)
            dists[neighbor] = dist + 1
    return dists[end]

def upsert(container,key,value):
    d = container.get(key,[])
    d.append(value)
    container[key] = d

def solve():
    orbits = util.load_data(fun=lambda x: x.split(')'))
    connexions = {}
    links = {}
    for k, v in orbits:
        upsert(connexions, k, v)
        upsert(links, v, k)
        upsert(links, k, v)

    print(f'Part1: {sum(path_length(connexions, c) for c in connexions)}')
    print(f'Part2: {path(connexions, links)}')

if __name__ == '__main__':
    solve()
