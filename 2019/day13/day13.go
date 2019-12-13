package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

var keys = map[int]string{
	0: " ",
	1: "|",
	2: "#",
	3: "_",
	4: "0",
}

type parameter struct {
	mode  int
	value int
}

func newParam(mode, value int) parameter {
	return parameter{
		mode:  mode,
		value: value,
	}
}

type program struct {
	data   []int
	rb     int
	ip     int
	input  []int
	output []int
	grid   [][]string
	score  int
	ball   int
	paddle int
	blocks int
}

func new(data []int) program {
	p := program{
		data:   data,
		rb:     0,
		ip:     0,
		input:  nil,
		output: nil,
	}
	return p
}

func (p *program) run() int {
	for {
		opcode, modes := parseOpcode(p.data[p.ip])
		if opcode == 99 {
			fmt.Println("Your score is: ", p.score)
			fmt.Println("This program has ended")
			return p.score
		}
		start := p.ip + 1
		end := start + numOfParams(opcode)
		rawParams := p.data[start:end]
		params := makeParams(rawParams, modes)
		p.compute(opcode, params)
		if p.ip == start-1 {
			p.ip = end
		}
	}
}

func (p *program) compute(opcode int, params []parameter) {
	switch opcode {
	case 1, 2, 7, 8:
		p1 := p.get(params[0])
		p2 := p.get(params[1])
		writer := params[2]
		var value int
		switch opcode {
		case 1:
			value = p1 + p2
		case 2:
			value = p1 * p2
		case 7:
			if p1 < p2 {
				value = 1
			}
		case 8:
			if p1 == p2 {
				value = 1
			}
		}
		p.set(writer, value)

	case 5, 6:
		p1 := p.get(params[0])
		p2 := p.get(params[1])
		switch opcode {
		case 5:
			if p1 != 0 {
				p.ip = p2
				return
			}
		case 6:
			if p1 == 0 {
				p.ip = p2
				return
			}
		}

	case 3, 4, 9:
		p1 := params[0]
		switch opcode {
		case 3:

			// i := p.prompt()
			// p.input = p.input[1:]
			var i int
			if p.ball < p.paddle {
				i = -1
			} else if p.ball > p.paddle {
				i = 1
			} else {
				i = 0
			}
			p.set(p1, i)
		case 4:
			p.output = append(p.output, p.get(p1))
			if len(p.output) == 3 {
				x, y, z := p.output[0], p.output[1], p.output[2]
				p.output = nil
				if x == -1 && y == 0 {
					p.score = z
				} else {
					if z == 3 {
						p.paddle = x
					} else if z == 4 {
						p.ball = x
					} else if z == 2 {
						p.blocks++
					}
					p.grid[y][x] = keys[z]
				}
				p.output = nil
			}
		case 9:
			p.rb += p.get(p1)
		}
	}

}

func (p *program) get(param parameter) int {
	switch param.mode {
	case 0:
		return p.data[param.value]
	case 1:
		return param.value
	case 2:
		return p.data[p.rb+param.value]
	}
	return 0
}

func (p *program) set(w parameter, value int) {
	if w.mode == 2 {
		w.value += p.rb
	}
	if w.value >= len(p.data) {
		p.grow(w.value + 1 - len(p.data))
	}
	p.data[w.value] = value
}

func (p *program) grow(size int) {
	d := make([]int, len(p.data)+size)
	for i := 0; i < len(p.data); i++ {
		d[i] = p.data[i]
	}
	p.data = d
}

func (p *program) prompt() int {
	printGrid(p.grid)
	fmt.Print("Enter direction: ")
	var input string
	fmt.Scanln(&input)
	if strings.EqualFold("a", input) {
		return -1
	} else if strings.EqualFold("d", input) {
		return 1
	} else {
		return 0
	}
}

func numOfParams(opcode int) int {
	switch opcode {
	case 1, 2, 7, 8:
		return 3
	case 3, 4, 9:
		return 1
	case 5, 6:
		return 2
	}
	return 0
}

func setup() []int {
	data, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	intcode := make([]int, 0, len(data))
	for _, s := range strings.Split(string(data), ",") {
		number, err := strconv.Atoi(s)
		if err != nil {
			fmt.Printf("%s is not an integer", s)
			continue
		}
		intcode = append(intcode, number)
	}
	return intcode
}

func parseOpcode(op int) (int, []int) {
	var modes []int
	if op < 100 {
		return op, modes
	}
	o := op % 100
	m := op / 100
	for m != 0 {
		modes = append(modes, m%10)
		m /= 10
	}
	return o, modes
}

func makeParams(params, modes []int) []parameter {
	pm := make([]parameter, 0, len(params))
	for i, value := range params {
		mode := 0
		if i < len(modes) {
			mode = modes[i]
		}
		pm = append(pm, newParam(mode, value))
	}
	return pm
}

func printGrid(grid [][]string) {
	for i := len(grid) - 1; i >= 0; i-- {
		s := strings.Join(grid[i], "")
		fmt.Println(s)
	}
}

func makeGrid(l, h int) [][]string {
	grid := make([][]string, 0, h)
	for i := 0; i < h; i++ {
		a := make([]string, 0, l)
		for j := 0; j < l; j++ {
			a = append(a, ".")
		}
		grid = append(grid, a)
	}
	return grid
}

func part1(intcode []int) {
	grid := makeGrid(44, 20)
	game := new(intcode)
	game.grid = grid
	game.run()
	fmt.Println(game.blocks)

}

func part2(intcode []int) {
	grid := makeGrid(44, 20)
	game := new(intcode)
	game.grid = grid
	game.data[0] = 2
	fmt.Println(game.run())
}

func main() {
	intcode := setup()
	part1(intcode)
	part2(intcode)
}
