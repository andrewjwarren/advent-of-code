#!/usr/bin/env python3

import itertools
from collections import deque


FEEDBACK_LOOP_ENABLED = True

num_of_parameters = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 1
}

colors_to_num = {
    ".": 0, # black
    "#": 1, # white
}

direction = {
    'left': '>',
    'up': '^',
    'right': '>',
    'down': 'v',
}

class brains:

    def __init__(self, data, inputs=None):
        self.data = data.copy()
        self._output = deque()
        self._input = deque()
        self.instruction_pointer = 0
        self.end = 0
        if inputs is not None:
            self.input = inputs
        self.completed = False
        self.relative_base = 0
        self.num_of_instructions = 0

    @property
    def input(self):
        return self._input.popleft()

    @input.setter
    def input(self, v):
        try:
            self._input.extend(v)
        except TypeError:
            self._input.append(v)

    @property
    def output(self):
        return self._output.popleft()

    @output.setter
    def output(self, v):
        self._output.append(v)

    def run(self):
        while True:
            start = self.instruction_pointer
            opcode, param_modes = parse_opcode(self.data[start])
            if opcode == 99:
                print('this progrom has ended')
                self.completed = True
                return

            self.end = start + num_of_parameters[opcode] + 1
            parameters = self.data[start + 1:self.end]
            params = list(itertools.zip_longest(param_modes,
                                                parameters,
                                                fillvalue=0))

            self.compute(opcode, params)
            self.num_of_instructions += 1
            if len(self._output) > 1 and FEEDBACK_LOOP_ENABLED:
                return

    def compute(self, opcode, params):
        def parameter_value(mode_and_param, array):
            mode, param = mode_and_param
            if mode == 0:
                return self.get_data(param)
            elif mode == 1:
                return param
            elif mode == 2:
                return self.get_data(self.relative_base + param)

        # These opcodes compare 2 params and write to the location of the 3rd
        if opcode in [1, 2, 7, 8]:
            p1 = parameter_value(params[0], self.data)
            p2 = parameter_value(params[1], self.data)
            writer = params[-1]
            value = 0
            if opcode == 1:
                value = p1 + p2
            elif opcode == 2:
                value = p1 * p2
            elif opcode == 7:
                if p1 < p2:
                    value = 1
            elif opcode == 8:
                if p1 == p2:
                    value = 1
            if value is None:
                print(self.instruction_pointer)
                raise

            self.write_data(writer, value)

        # These opcodes reassign the terminal pointer
        elif opcode in [5, 6]:
            p1 = parameter_value(params[0], self.data)
            p2 = parameter_value(params[1], self.data)
            if opcode == 5:
                if p1 != 0:
                    self.instruction_pointer = p2
                    return
            elif opcode == 6:
                if p1 == 0:
                    self.instruction_pointer = p2
                    return

        # These opcodes only take one parameter
        elif opcode in [3, 4, 9]:
            p1 = params[0]
            if opcode == 3:
                self.write_data(p1, self.input)
            elif opcode == 4:
                self.output = parameter_value(p1, self.data)
            elif opcode == 9:
                self.relative_base += parameter_value(p1, self.data)

        self.instruction_pointer = self.end

    def reset(self):
        self.instruction_pointer = 0

    def write_data(self, k, v):
        mode, pos = k
        if mode == 2:
            pos += self.relative_base
        try:
            self.data[pos] = v
        except IndexError:
            self._grow(pos + 1 - len(self.data))
            self.data[pos] = v

    def get_data(self, k):
        try:
            return self.data[k]
        except IndexError:
            return 0

    def _grow(self, size):
        for x in range(size + 1):
            self.data.append(0)

    def move(direction):
        pass


num_to_color = {
    0: '.', # black
    1: '#'  # white

}

class robot:
    def __init__(self, intcode, start=(0,0), size=None):
        self.x, self.y = start
        self.direction = '^'
        self.current_color = 0
        self.previous_color = 0
        self.grid = []
        if size is None:
            self._make_grid(50, 50)
        else:
            self._make_grid(*size)
        self.visited = set()
        self.brains = brains(intcode)
        self.grid[self.y][self.x] = self.direction
        self.brains.input = 1
        self.print_grid()



    def print_grid(self):
        k = []
        for x in reversed(self.grid):
            n = "".join(x)
            k.append(n)
        print("\n".join(k))

    def _make_grid(self, x, y):
        for i in range(y):
            self.grid.append(['.' for i in range(x)])

    def _move_robot(self, x, y, color='.'):
        current = (self.x, self.y)

        # provide the input to the brains of color of tile moving to
        n = self.grid[y][x]
        self.brains.input = colors_to_num[n]

        # move robot
        self.grid[y][x] = self.direction
        self.x, self.y = x, y

        # paint previous square accoring to brains output
        self.paint_square(*current, self.previous_color)
        
        self.print_grid()

    def run(self):
        self.brains.run()
        self.previous_color = self.brains.output
        rotation = self.brains.output
        if rotation == 0:
            self.rotate_left()
        elif rotation == 1:
            self.rotate_right()

    def paint_square(self, x, y, color):
        self.visited.add((x,y))
        self.grid[y][x] = num_to_color[color]

    def rotate_left(self):
        direction = {
            '^': '<',
            '<': 'v',
            'v': '>',
            '>': '^'
        }
        d = direction[self.direction]
        self._rotate(d)

    def rotate_right(self):
        direction = {
            '^': '>',
            '>': 'v',
            'v': '<',
            '<': '^'
        }
        d = direction[self.direction]
        self._rotate(d)

    def _rotate(self, d):
        self.direction = d
        if d in ['^', 'v']:
            y = self.y
            if d == '^':
                y += 1
            elif d == 'v':
                y -= 1
            self._move_robot(self.x, y)
        
        if d in ['<', '>']:
            x = self.x
            if d == '>':
                x += 1
            elif d == '<':
                x -= 1
            self._move_robot(x, self.y)


def parse_opcode(opcode):
    if opcode < 10:
        return (opcode, [])
    else:
        op = opcode % 100
        params = opcode // 100
        pos_nums = []
        while params != 0:
            pos_nums.append(params % 10)
            params //= 10
        return (op, pos_nums)


def phase_settings(low, high):
    for x in itertools.permutations(range(low, high)):
        yield x



if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().split(',')
    intcode = [int(x) for x in data]
    r = robot(intcode, (24,24), (100, 100))
    while True:
        try:
            r.run()
        except IndexError:
            print(len(r.visited))
            break
