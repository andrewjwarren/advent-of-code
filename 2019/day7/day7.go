package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type parameter struct {
	value int
	mode  int
}

func execute(intcode []int, noun, verb int) int {
	newArray := append([]int(nil), intcode...)
	newArray[1] = noun
	newArray[2] = verb
	v := readIntcode(newArray)
	return v[0]
}

func parseOpcode(opcode int) (int, []int) {
	code := strconv.Itoa(opcode)
	var o int
	var p []int
	if len(code) < 3 {
		o, _ = strconv.Atoi(code)
	} else {
		o, _ = strconv.Atoi(code[len(code)-2:])
		for i := len(code) - 2; i >= 0; i-- {
			mode, _ := strconv.Atoi(string(code[i]))
			p = append(p, mode)
		}
	}
	return o, p
}

func makeParameters(modes, params []int) []parameter {
	var combined []parameter
	for i, param := range params {
		mode := 0
		if i < len(modes) {
			mode = modes[i]
		}
		p := parameter{
			mode:  mode,
			value: param,
		}
		combined = append(combined, p)
	}
	return combined
}

// func opcode_1(params []parameter, data []int, end int) {

// }

var numPositions = map[int]int{
	1: 3,
	2: 3,
	3: 1,
	4: 1,
	5: 2,
	6: 2,
	7: 3,
	8: 3,
}

func paramValues(params []parameter, data []int) (int, int, int) {
	p := make([]int, 0, 3)
	for _, param := range params {
		if param.mode == 1 {
			p = append(p, param.value)
		} else {
			p = append(p, data[param.value])
		}
	}
	return p[0], p[1], p[2]
}

func readIntcode(data []int) []int {
	instructionPointer := 0
	end := 0
	for {
		opcode, modes := parseOpcode(data[instructionPointer])
		end = instructionPointer + 1 + numPositions[opcode]
		p := data[instructionPointer+1 : end]
		params := makeParameters(modes, p)

		if opcode == 1 {
			data[paramValue(params[0])] = paramValue(params[0]) + paramValue(params[1])
		} else if opcode == 2 {
			data[pos3] = data[pos1] * data[pos2]
		} else if opcode == 99 {
			break
		}
		instructionPointer = end
	}
	return data
}

func main() {
	data, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	intcode := make([]int, 0, 10)
	for _, s := range strings.Split(string(data), ",") {
		number, err := strconv.Atoi(s)
		if err != nil {
			fmt.Printf("%s is not an integer", s)
			continue
		}
		intcode = append(intcode, number)
	}
	k := readIntcode([]int{2, 4, 3, 4, 99})
	fmt.Println(k)
}
