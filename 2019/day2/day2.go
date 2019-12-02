package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func execute(intcode []int, noun, verb int) int {
	newArray := append([]int(nil), intcode...)
	newArray[1] = noun
	newArray[2] = verb
	for start := 0; start+4 <= len(newArray); start += 4 {
		opcode := newArray[start]
		pos1 := newArray[start+1]
		pos2 := newArray[start+2]
		pos3 := newArray[start+3]
		if opcode == 1 {
			newArray[pos3] = newArray[pos1] + newArray[pos2]
		} else if opcode == 2 {
			newArray[pos3] = newArray[pos1] * newArray[pos2]
		} else if opcode == 99 {
			break
		}
	}
	return newArray[0]
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
