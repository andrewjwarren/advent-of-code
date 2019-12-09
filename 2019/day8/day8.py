#!/usr/bin/env python3

LENGTH = 25
HEIGHT = 6

COLORS = {
    0: " ",
    1: "X"
}


def make_layers(data, h, l):
    layers = []
    size = h * l
    for x in range(0, len(data), size):
        layers.append(data[x:x + size])
    return layers


def fewest_zeros(layers):
    layer = 0
    num_of_zeros = LENGTH
    for i, x in enumerate(layers):
        a = x.count(0)
        if a < num_of_zeros:
            num_of_zeros = a
            layer = i
    return layers[layer]


def make_image(code):
    code = [COLORS[x] for x in code]
    for x in range(0, len(code), LENGTH):
        print("".join(code[x:x+LENGTH]))


def decode_layers(layers):
    code = []
    for pixel in range(LENGTH * HEIGHT):
        for layer in layers:
            color = layer[pixel]
            if color != 2:
                code.append(color)
                break
    return code


def part1(layers):
    fewest = fewest_zeros(layers)
    return fewest.count(1) * fewest.count(2)


def part2(layers):
    code = decode_layers(layers)
    make_image(code)


if __name__ == "__main__":
    with open('input.txt') as f:
        data = list(map(int, f.read()))

    layers = make_layers(data, HEIGHT, LENGTH)
    print(part1(layers))
    part2(layers)
