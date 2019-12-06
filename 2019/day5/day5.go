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
	o := 0
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

func readIntcode(data []int) []int {
	instructionPointer := 0
	for {
		opcode := data[instructionPointer]
		pos1 := data[instructionPointer+1]
		pos2 := data[instructionPointer+2]
		pos3 := data[instructionPointer+3]
		if opcode == 1 {
			data[pos3] = data[pos1] + data[pos2]
		} else if opcode == 2 {
			data[pos3] = data[pos1] * data[pos2]
		} else if opcode == 99 {
			break
		}
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

	for noun := 0; noun < 100; noun++ {
		completed := false
		for verb := 0; verb < 100; verb++ {
			result := execute(intcode, noun, verb)
			if result == 19690720 {
				fmt.Println(100*noun + verb)
				completed = true
				break
			}
			if completed {
				break
			}
		}
	}
}
