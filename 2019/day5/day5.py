#!/usr/bin/env python3

import itertools

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

def read_intcode(data):
    instruction_pointer = 0
    while True:
        opcode, param_modes = parse_opcode(data[instruction_pointer])
        if opcode == 99:
            break 
        try:
            end = instruction_pointer + num_of_parameters[opcode] + 1
            parameters = data[instruction_pointer + 1:end]
            combined = list(itertools.zip_longest(param_modes, parameters, fillvalue=0))
        except IndexError:
            print('Ran to the end of the data')
            break
        except KeyError:
            print('Unknown opcode: {}'.format(opcode))
            break
        
        zipped = list(itertools.zip_longest(param_modes, parameters, fillvalue=0))

        op = opcode_operation(opcode)
        value = op(zipped, data, end)
        if value:
            end = value
        instruction_pointer = end
    return data

def execute(data, noun, verb):
    new_array = data[:]
    new_array[1] = noun
    new_array[2] = verb
    instruction_pointer = 0
    return read_intcode(new_array)

def opcode_1(params, data, end):
    p1, p2, writer = params
    data[writer[-1]] = parameter_value(p1, data) + parameter_value(p2, data)

def opcode_2(params, data, end):
    p1, p2, writer = params
    data[writer[-1]]  = parameter_value(p1, data) * parameter_value(p2, data)

def opcode_3(params, data, end):
    writer = params[0]
    value = int(input('Unit ID\n'))
    data[writer[-1]] = value

def opcode_4(params, data, end):
    p1 = params[0]
    output = parameter_value(p1, data)
    print(output)

def opcode_5(params, data, end):
    p1, p2 = params
    if parameter_value(p1, data):
        return parameter_value(p2, data)
    return end

def opcode_6(params, data, end):
    p1, p2 = params
    if parameter_value(p1, data) == 0:
        return parameter_value(p2, data)
    return end

def opcode_7(params, data, end):
    p1, p2, writer = params
    value = 0
    if parameter_value(p1, data) < parameter_value(p2, data):
        value = 1
    data[writer[-1]] = value

def opcode_8(params, data, end):
    p1, p2, writer = params
    value = 0
    if parameter_value(p1, data) == parameter_value(p2, data):
        value = 1
    data[writer[-1]] = value

def opcode_operation(opcode):
    operation = {
        1: opcode_1,
        2: opcode_2,
        3: opcode_3,
        4: opcode_4,
        5: opcode_5,
        6: opcode_6,
        7: opcode_7,
        8: opcode_8
    }
    return operation[opcode]

def parse_opcode(opcode):
    opcode = str(opcode)
    op, parameter_modes = int(opcode[-2:]), opcode[:-2]
    modes = [int(x) for x in reversed(parameter_modes)] 
    return (op, modes)

def parameter_value(mode_and_param, array):
    mode, param = mode_and_param
    if mode == 1:
        return param
    return array[param]

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().split(',')
        intcode = [int(x) for x in data]
        result = read_intcode(intcode)

        
        