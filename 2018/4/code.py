#!/usr/bin/env python
import re
from datetime import datetime
from collections import defaultdict

def load_input(input_file):
    with open(input_file, 'r') as fp:
        events = [line for line in fp.read().splitlines()]
    return events


def process(events):

    _ptn = re.compile(
        r'\[(?P<timestamp>[^\]]+)\]\s+'
        r'(?:Guard\s+#(?P<guard>\d+)\s+)?'
        r'(?P<transition>.*)').search

    events.sort()
    guards=defaultdict(lambda: [0]*60)

    for event in events:
        match = _ptn(event)
        if match is None:
            raise ValueError(f'Unparsable event line {event!r}')
        evt = match.groupdict()
        ts = datetime.strptime(evt['timestamp'],'%Y-%m-%d %H:%M')
        if evt['transition'] == 'begins shift':
            guard = int(evt['guard'])
        elif evt['transition'] == 'falls asleep':
            start_sleep = ts.minute
        elif evt['transition'] == 'wakes up':
            end_sleep = ts.minute
            for i in range(start_sleep, end_sleep):
                guards[guard][i] +=1


    guard_p1, _ = max([(k, sum(v)) for k,v in guards.items()],
                      key=lambda x: x[1])
    minute_p1 = guards[guard_p1].index(max(guards[guard_p1]))

    p1 = guard_p1 * minute_p1

    guard_p2, ip2 = max([(k, max(v)) for k,v in guards.items()],
                        key=lambda x: x[1])
    minute_p2 = guards[guard_p2].index(ip2)
    p2 = guard_p2 * minute_p2

    print('Result for part one is {}.'.format(p1))
    print('Result for part two is {}.'.format(p2))

if __name__ == "__main__":
    process(load_input('input'))
