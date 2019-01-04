#!/usr/bin/env python

INTIAL_scores = '37'

def process(skill):
    part1 = part2 = None
    scores = [int(r) for r in INTIAL_scores]
    skills = [int(r) for r in skill]
    first_elf = 0
    second_elf = 1

    while len(scores) < int(skill) + 10:
        scores += [int(x) for x in str(scores[first_elf] + scores[second_elf])]
        first_elf = (first_elf + scores[first_elf] + 1) % len(scores)
        second_elf = (second_elf + scores[second_elf] + 1) % len(scores)

    part1 = ''.join(map(str, scores[int(skill):int(skill)+10]))

    return part1, part2


    # all(e in l1 for e in l2)

    return (part1, part2)

if __name__ == '__main__':
    assert ('5158916779', None) == process('9')
    assert ('0124515891', None) == process('5')
    assert ('9251071085', None) == process('18')
    assert ('5941429882', None) == process('2018')
    print(process('074501'))
