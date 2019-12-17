#!/usr/bin/env python3

PATTERN = [1, 0, -1, 0]


def grow_pattern(element, size):
    while size > 0:
        for x in [0, 1, 0, -1]:
            for _ in range(element + 1):
                yield x
                size -= 1


def generate_output(data):
    total = 0
    for pair in data:
        total += pair[0] * pair[1]
    return abs(total) % 10


def part1(read, num_of_phases):
    maybe = []
    # Phase Loop
    for x in range(num_of_phases):
        # Element Loop
        for i in range(len(read)):
            pattern = grow_pattern(i, len(read))
            next(pattern)
            data = zip(read, pattern)
            total = generate_output(data)
            maybe.append(total)
        # print(maybe)
        read = maybe[:]
        maybe = []
    return "".join([str(x) for x in read])[:8]


def part2(read):
    data = read * 10000
    offset = int("".join([str(x) for x in data[:7]]))
    data = data[offset:]
    for _ in range(100):
        total = 0
        for i in range(len(data)-1, -1, -1):
            total += data[i]
            data[i] = total % 10
    return "".join([str(x) for x in data[:8]])



if __name__ == '__main__':
    with open('input.txt') as f:
        phase1 = f.read()
    
    # phase1 = '03036732577212944063491565474664'

    read = [int(x) for x in phase1]
    print(part1(read, 100))
    print(part2(read))