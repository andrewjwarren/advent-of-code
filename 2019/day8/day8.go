package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
)

const HEIGHT = 6
const LENGTH = 25
const SIZE = HEIGHT * LENGTH

var COLORS = map[int]string{
	0: " ",
	1: "X",
}

func setup() []int {
	data, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}

	image := make([]int, 0, len(data))
	for _, i := range string(data) {
		j, _ := strconv.Atoi(string(i))
		image = append(image, j)
	}
	return image
}

func makeLayers(image []int) [][]int {
	layers := make([][]int, 0, HEIGHT)
	for i := 0; i < len(image); i += SIZE {
		layer := image[i : i+SIZE]
		layers = append(layers, layer)
	}
	return layers
}

func fewestZeros(layers [][]int) []int {
	layer := 0
	numZeros := LENGTH
	for i, j := range layers {
		c := count(0, j)
		if c < numZeros {
			numZeros = c
			layer = i
		}
	}
	return layers[layer]
}

func count(number int, layer []int) int {
	count := 0
	for _, i := range layer {
		if i != number {
			continue
		}
		count++
	}
	return count
}

func part1(layers [][]int) int {
	fewest := fewestZeros(layers)
	return count(1, fewest) * count(2, fewest)
}

func part2(layers [][]int) {
	code := decodeLayers(layers)
	makeImage(code)
}

func makeImage(image []int) {
	code := func(i []int) []string {
		k := make([]string, 0, len(image))
		for _, c := range i {
			k = append(k, COLORS[c])
		}
		return k
	}(image)

	var layer string
	for i, s := range code {
		if i%LENGTH == 0 {
			fmt.Println(layer)
			layer = ""
		}
		layer += s
	}
	fmt.Println(layer)
}

func decodeLayers(layers [][]int) []int {
	code := make([]int, 0, HEIGHT*LENGTH)
	for pixel := 0; pixel < SIZE; pixel++ {
		for _, layer := range layers {
			color := layer[pixel]
			if color != 2 {
				code = append(code, color)
				break
			}
		}
	}
	return code
}

func main() {
	code := setup()
	layers := makeLayers(code)
	fmt.Println(part1(layers))
	part2(layers)
}
