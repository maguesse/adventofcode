#!/usr/bin/env python

def load_input(input_file):
    with open(input_file, 'r') as fp:
        frequencies = [int(line) for line in fp]
    return frequencies

def do_it(frequencies,
          frequency=0,
          seen=None,
          reached_twice=None,
          part=1):
    if seen is None:
        seen = set()
        seen.add(frequency)
    for freq in frequencies:
        frequency += freq
        if frequency in seen:
            reached_twice = frequency
            if part > 1:
                break
        seen.add(frequency)
    return (frequency, seen, reached_twice)

def process(frequencies,
            frequency=0):
    frequency, seen, reached_twice = do_it(frequencies, part=1)
    print('Part one result : {}'.format(frequency))

    while reached_twice is None:
        frequency, seen, reached_twice = do_it(frequencies, frequency, seen,
                                               reached_twice, part=2)

    print('Part two result : {}'.format(reached_twice))

if __name__ == "__main__":
    process(load_input('input'))
