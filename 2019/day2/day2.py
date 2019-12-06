#!/usr/bin/env python3

import itertools

num_of_parameters = {
    1: 3,
    2: 3,
    3: 1,
    4: 1
}

# execute([1,0,0,0,99], 0, 0)
def read_intcode(data):
    instruction_pointer = 0
    while True:
        opcode, param_modes = parse_opcode(data[instruction_pointer])
        if opcode == 99:
            break 
        try:
            end = instruction_pointer + num_of_parameters[opcode] + 1
            parameters = data[instruction_pointer + 1:end]
        except IndexError:
            print('Ran to the end of the data')
            break
        except KeyError:
            print('Unknown opcode: {}'.format(opcode))
            break

        if opcode == 1:
            p1, p2, writer = itertools.zip_longest(param_modes, parameters, fillvalue=0)
            data[writer[1]] = parameter_value(p1, data) + parameter_value(p2, data)
        elif opcode == 2:
            p1, p2, writer = itertools.zip_longest(param_modes, parameters, fillvalue=0)
            data[writer[1]]  = parameter_value(p1, data) * parameter_value(p2, data)
        elif opcode == 3:
            print(parameters)
            writer = parameters[0]
            value = int(input('Unit ID\n'))
            data[writer] = value
        elif opcode == 4:
            print(parameters[0])
        instruction_pointer = end
    return data


def execute(data, noun, verb):
    new_array = data[:]
    new_array[1] = noun
    new_array[2] = verb
    instruction_pointer = 0
    return read_intcode(new_array)

# # instructions are the whole thing
# # opcode is first
# # parameters

# def opcode_operation(opcode, parameters):
#     operations = {
#         1: lambda x, y: x + y,
#         2: lambda x, y: x * y,
#         3: lambda x: x=input,
#         4: lambda x: print(x),
#     }
#     return operations.get(opcode, None)

# instructions are the whole thing
# opcode is first
# parameters are everything that follows
def parse_instructions(instructions):
    opcode, parameters = str(instructions[0]), instructions[1:]
    opcode, parameter_modes = opcode[-2:], opcode[:-2]
    if len(parameter_modes) < len(parameters):
        parameter_modes = '0' * (len(parameters) - len(parameter_modes)) + parameter_modes
    modes = [int(x) for x in reversed(parameter_modes)]
    l = list(zip(modes, parameters))
    return int(opcode), l

def parse_opcode(opcode):
    opcode = str(opcode)
    opcode, parameter_modes = int(opcode[-2:]), opcode[:-2]
    modes = [int(x) for x in reversed(parameter_modes)]
    return (opcode, modes)

def parameter_value(mode_and_param, array):
    mode, param = mode_and_param
    if mode == 1:
        return param
    return array[param]


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().split(',')
        intcode = [int(x) for x in data]
        for noun in range(0, 100):
            completed = False
            for verb in range(0, 100):
                result = execute(intcode, noun, verb)
                if result[0] == 19690720:
                    print(100 * noun + verb)
                    completed = True
                    break
            if completed:
                break
        
        