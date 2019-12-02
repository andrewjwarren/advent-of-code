#!/usr/bin/env python3

def execute(data, noun, verb):
    new_array = data[:]
    new_array[1] = noun
    new_array[2] = verb
    start = 0
    while start + 4 <= len(new_array):
        end = start + 4
        opcode, pos1, pos2, pos3 = new_array[start:end]
        if opcode == 1:
            new_array[pos3] = new_array[pos1] + new_array[pos2]
        elif opcode == 2:
            new_array[pos3] = new_array[pos1] * new_array[pos2]
        elif opcode == 99:
            break
        start = end
    return new_array[0]

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().split(',')
        intcode = [int(x) for x in data]
        for noun in range(0, 100):
            completed = False
            for verb in range(0, 100):
                result = execute(intcode, noun, verb)
                if result == 19690720:
                    print(100 * noun + verb)
                    completed = True
                    break
            if completed:
                break
        
        