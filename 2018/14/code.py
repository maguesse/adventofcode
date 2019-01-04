#!/usr/bin/env python

INTIAL_scores = '37'

def process(skill):
    part1 = part2 = None
    #scores = [int(r) for r in INTIAL_scores]
    scores = INTIAL_scores
    first_elf = 0
    second_elf = 1

    len_skill = len(skill)+1

    while skill not in scores[-len_skill:]:
        scores += str(int(scores[first_elf]) + int(scores[second_elf]))
        first_elf = (first_elf + int(scores[first_elf]) + 1) % len(scores)
        second_elf = (second_elf + int(scores[second_elf]) + 1) % len(scores)

    part1 = scores[int(skill):int(skill)+10]
    part2 = scores.index(skill)

    print(f'Part1:{part1}, Part2:{part2}')

    return (part1, part2)

if __name__ == '__main__':
    process('9')
    process('5')
    process('18')
    process('2018')
    process('074501')
