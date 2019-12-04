#!/usr/bin/env python3

class Wire:
    def __init__(self): 
        self.current = (0,0)
        self.points = {}
        self._counter = 0

    def right(self, spaces):
        x, y = self.current
        for _ in range(spaces):
            x += 1
            self._update((x,y))

    def left(self, spaces):
        x, y = self.current
        for _ in range(spaces):
            x -= 1
            self._update((x,y))

    def up(self, spaces):
        x, y = self.current
        for _ in range(spaces):
            y += 1
            self._update((x,y))

    def down(self, spaces):
        x, y = self.current
        for _ in range(spaces):
            y -= 1
            self._update((x,y))

    def _add_to_steps(self, point):
        if point in self.steps:
            return
        self.steps[point] = self._counter
    
    def _update(self, point):
        self._counter += 1
        self.current = point
        try:
            _ = self.points[point]
            return
        except KeyError:
            self.points[point] = self._counter
        

def build_wire(instructions):
    wire = Wire()
    for instruction in instructions.split(','):
        direction, spaces = instruction[0], int(instruction[1:])
        if direction == "R":
            wire.right(spaces)
        elif direction == "L":
            wire.left(spaces)
        elif direction == "U":
            wire.up(spaces)
        elif direction == "D":
            wire.down(spaces)
    return wire

def find_intersections(wire1, wire2):
    intersections = set()
    for w1 in wire1.points.keys():
        try:
            intersect = wire2.points[w1]
            intersections.add(w1)
        except KeyError:
            continue
    return list(intersections)

def distance_to_start(point):
    x, y = point
    return abs(x) + abs(y)

def steps_from_start(point, wire1, wire2):
    w1 = wire1.points[point]
    w2 = wire2.points[point]
    return w1 + w2

if __name__ == '__main__':
    
    with open('input.txt') as f:
        data = f.read().split()

    wire1 = build_wire(data[0])
    wire2 = build_wire(data[1])
    intersections = find_intersections(wire1, wire2)
    
    shortest = 0 
    for x in range(len(intersections)):
        dist = distance_to_start(intersections[x])
        if x == 0:
                shortest = dist
        elif dist < shortest:
                shortest = dist
    print(shortest)

    fewest_steps = 0
    for x in range(len(intersections)):
        steps = steps_from_start(intersections[x], wire1, wire2)
        if x == 0:
                fewest_steps = steps
        elif steps < fewest_steps:
                fewest_steps = steps
    print(fewest_steps)