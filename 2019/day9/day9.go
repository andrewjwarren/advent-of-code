package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

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
	data    []int
	rb      int
	ip      int
	inputs  chan int
	outputs chan int
}

func new(data []int) program {
	p := program{
		data:    data,
		rb:      0,
		ip:      0,
		inputs:  make(chan int, 2),
		outputs: make(chan int, 2),
	}
	return p
}

func (p *program) run() {
	for {
		opcode, modes := parseOpcode(p.data[p.ip])
		if opcode == 99 {
			fmt.Println("This program has ended")
			return
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
			i := <-p.inputs
			p.set(p1, i)
		case 4:
			p.outputs <- p.get(p1)
		case 9:
			p.rb += p.get(p1)
		}
	}

}

func (p *program) addInput(i int) {
	if p.inputs == nil {
		p.inputs = make(chan int, 2)
	}
	p.inputs <- i
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

func part1(intcode []int) {
	p := new(intcode)
	p.addInput(1)
	p.run()
	fmt.Println(<-p.outputs)
}

func part2(intcode []int) {
	p := new(intcode)
	p.addInput(2)
	p.run()
	fmt.Println(<-p.outputs)
}

func main() {
	intcode := setup()
	part1(intcode)
	part2(intcode)
}
