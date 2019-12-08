#!/usr/bin/env python3

import itertools
from collections import deque


FEEDBACK_LOOP_ENABLED = False

num_of_parameters = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3
}


class Amplifier:

    def __init__(self, data, inputs=None):
        self.data = data.copy()
        self._output = deque()
        self._input = deque()
        self.instruction_pointer = 0
        self.end = 0
        if inputs is not None:
            self.input = inputs
        self._next = Amplifier
        self.completed = False

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

            try: 
                parameters = self.data[start + 1:self.end]
                params = list(itertools.zip_longest(param_modes,
                                                    parameters,
                                                    fillvalue=0))
            except IndexError:
                print('Ran to the end of the data')
                return
            except KeyError:
                print('Unknown opcode: {}'.format(opcode))
                return

            self.compute(opcode, params)
            if len(self._output) > 0:
                return

    def compute(self, opcode, params):

        def parameter_value(mode_and_param, array):
            mode, param = mode_and_param
            if mode == 1:
                return param
            return array[param]

        # These opcodes compare 2 params and write to the location of the 3rd
        if opcode in [1, 2, 7, 8]:
            p1 = parameter_value(params[0], self.data)
            p2 = parameter_value(params[1], self.data)
            writer = params[2][-1]
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
            self.data[writer] = value

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
        elif opcode in [3, 4]:
            p1 = params[0]
            if opcode == 3:
                self.data[p1[-1]] = self.input
            elif opcode == 4:
                self.output = parameter_value(p1, self.data)
                

        self.instruction_pointer = self.end

    def reset(self):
        self.instruction_pointer = 0


def parse_opcode(opcode):
    opcode = str(opcode)
    op, parameter_modes = int(opcode[-2:]), opcode[:-2]
    modes = [int(x) for x in reversed(parameter_modes)]
    return (op, modes)


def phase_settings(low, high):
    for x in itertools.permutations(range(low, high)):
        yield x


def part1(intcode):
    result = 0
    for settings in phase_settings(0, 5):
        output = 0
        for y in settings:
            amp = Amplifier(intcode, [y, output])
            amp.run()
            output = amp.output
        if output > result:
            result = output
    return result


def part2(intcode):
    result = 0
    for settings in phase_settings(5, 10):

        amps = []
        for y in settings:
            amp = Amplifier(intcode, y)
            amps.append(amp)
        output = 0
        for amp in itertools.cycle(amps):
            if amp.completed:
                break
            amp.input = output
            amp.run()
            try:
                output = amp.output
            except IndexError:
                break
        if output > result:
            result = output
    return result


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().split(',')
    intcode = [int(x) for x in data]
    print(part1(intcode))
    print(part2(intcode))
