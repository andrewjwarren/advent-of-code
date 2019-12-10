package main

import "testing"

func TestParseOpcode(t *testing.T) {
	inputs := []int{1002, 21108, 1}
	outputOpcodes := []int{2, 8, 1}
	outputModes := [][]int{
		{0, 1},
		{1, 1, 2},
		{},
	}
	for i, input := range inputs {
		op, modes := parseOpcode(input)
		if op != outputOpcodes[i] {
			t.Errorf("Got opcode %d expected %d", op, outputOpcodes[i])
		}
		for j, mode := range modes {
			if mode != outputModes[i][j] {
				t.Errorf("Got modes %v expected %v", modes, outputModes[i])
			}
		}
	}
}

func TestMakeParams(t *testing.T) {
	modes := []int{0, 1}
	params := []int{1, 2, 3}
	answers := []parameter{
		parameter{0, 1},
		parameter{1, 2},
		parameter{0, 3},
	}
	k := makeParams(params, modes)
	for i, param := range k {
		a := answers[i]
		if param.value != a.value {
			t.Errorf("Got %v Expected %v", param, a)
		} else if param.mode != a.mode {
			t.Errorf("Got %v Expected %v", param, a)
		}
	}
}

func TestGet(t *testing.T) {
	inputs := []parameter{
		{0, 1},
		{1, 1},
		{2, 2},
	}
	answers := []int{20, 1, 30}
	p := new([]int{10, 20, 30, 40})
	for i, input := range inputs {
		a := answers[i]
		b := p.get(input)
		if a != b {
			t.Errorf("Got %v Expected %v", b, a)
		}
	}
}

func TestSet(t *testing.T) {
	inputs := []parameter{
		{0, 10},
		{2, 20},
	}

	p := new([]int{0, 1, 2, 3, 4})

	for _, input := range inputs {
		p.set(input, 1)
		if p.data[input.value] != 1 {
			t.Errorf("Something went wrong")
		}
	}
}
