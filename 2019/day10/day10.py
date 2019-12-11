#!/usr/bin/env python3

import math
from collections import namedtuple, defaultdict
from operator import attrgetter

ASTROID = namedtuple("Astroid", 'x y angle distance')

VAPORIZED = 'The {} asteroid to be vaporized is at {}.'


def gridsize(grid):
    return (len(grid[0]), len(grid))


def find_astroids(grid):
    coordinates = {}
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "#":
                coordinates[(x, y)] = 0
    return coordinates


def gradiant(coordA, coordB):
    rise = coordA[-1] - coordB[-1]
    run = coordA[0] - coordB[0]
    if run == 0 or rise == 0:
        return 0
    return rise / run


def get_quadrants(coordinates, start):
    top_right = []
    bottom_right = []
    bottom_left = []
    top_left = []
    grid = [top_right, bottom_right, bottom_left, top_left] 
    for x, y in coordinates:
        a = ASTROID(x, y, angle(start, (x, y)), dist(start, (x, y)))
        if (x, y) == start:
            continue
        if y >= start[1]:
            if x >= start[0]:
                bottom_right.append(a)
            else:
                bottom_left.append(a)
        else:
            if x >= start[0]:
                top_right.append(a)
            else:
                top_left.append(a)
    for i in range(len(grid)):
        grid[i] = sorted(grid[i], key=attrgetter('angle', 'distance'))
        if i == 1:
            index = 0
            for j, v in enumerate(grid[i]):
                if v.angle >= 0:
                    index = j
                    break
            grid[i] = grid[i][index:] + grid[i][:index]
    return grid


def find_angles(coords, start):
    a = defaultdict(list)
    quads = get_quadrants(coords, start)
    for quad in quads:
        for coord in quad:
            a[coord.angle].append(coord)
    return a


def angle(a, b):
    return math.atan2(a[1] - b[1], a[0] - b[0])


def dist(a, b):
    return (math.sqrt((a[0] - b[0]) ** 2.0)) + (math.sqrt((a[1] - b[1]) ** 2.0))


def part1(grid):
    astroids = find_astroids(grid)
    keys = [x for x in astroids.keys()]
    for astroid in keys:
        a = find_angles(keys, astroid)
        astroids[astroid] = len(a)
    highest = 0
    coord = 0
    for k, v in astroids.items():
        if v > highest:
            highest = v
            coord = k
    return (coord, highest)


def part2(grid, start):
    astroids = find_astroids(grid)
    quads = get_quadrants(astroids.keys(), start)
    num = 1
    completed = 0
    while completed < 4:
        for i, quad in enumerate(quads):
            if len(quad) < 1:
                continue
            last = 100
            leftovers = []
            for roid in quad:
                if roid.angle == last:
                    leftovers.append(roid)
                    continue
                print(VAPORIZED.format(num, (roid.x, roid.y)))
                last = roid.angle
                num += 1
            quads[i] = leftovers
            if len(leftovers) == 0:
                completed += 1


if __name__ == '__main__':

    with open('input.txt') as f:
        grid = f.read().split()

    start, highest = part1(grid)
    print(highest)
    part2(grid, start)

    # w = []

    # order = [(8, 1),
    #         (9, 0),
    #         (9, 1),
    #         (10, 0),
    #         (9, 2),
    #         (11, 1),
    #         (12, 1),
    #         (11, 2),
    #         (15, 1),
    #         (12, 2),
    #         (13, 2),
    #         (14, 2),
    #         (15, 2),
    #         (12, 3),
    #         (16, 4),
    #         (15, 4),
    #         (10, 4),
    #         (4, 4),
    #         (2, 4),
    #         (2, 3),
    #         (0, 2),
    #         (1, 2),
    #         (0, 1),
    #         (1, 1)]

    # for i, x in enumerate(order):
    #     if x != (w[i].x, w[i].y):
    #         print('nope {}'.format(x))



    # what = defaultdict(list)
    # for quad in quads:
    #     for roid in quad:
    #         what[roid.angle].append(roid)

        
# The 14 asteroid to be vaporized is at .
# The 15 asteroid to be vaporized is at .
# The 16 asteroid to be vaporized is at .


# The 18 asteroid to be vaporized is at .
# The 19 asteroid to be vaporized is at .

# The 20 asteroid to be vaporized is at .
# The 21 asteroid to be vaporized is at .
# The 22 asteroid to be vaporized is at .
# The 23 asteroid to be vaporized is at .
# The 24 asteroid to be vaporized is at .
# The 25 asteroid to be vaporized is at (5, 2).
# The 26 asteroid to be vaporized is at (1, 0).
# The 27 asteroid to be vaporized is at (5, 1).
# The 28 asteroid to be vaporized is at (6, 1).
# The 29 asteroid to be vaporized is at (6, 0).
# The 30 asteroid to be vaporized is at (7, 0).
# The 31 asteroid to be vaporized is at (8, 0).
# The 32 asteroid to be vaporized is at (10, 1).
# The 33 asteroid to be vaporized is at (14, 0).
# The 34 asteroid to be vaporized is at (16, 1).
# The 35 asteroid to be vaporized is at (13, 3).
# The 36 asteroid to be vaporized is at (14, 3).