package main

import (
	"testing"
)

func TestParseOpcode(t *testing.T) {
	opcode := 1002
	v, _ := parseOpcode(opcode)
	if v != 2 {
		t.Errorf("opscode: %d expected: %d", v, 2)
	}

}

func TestMakeParameters(t *testing.T) {
	modes := []int{1, 1}
	params := []int{2, 2, 2}
	v := makeParameters(modes, params)
	for i, param := range v {
		if i == 2 {
			if param.mode != 0 || param.value != 2 {
				t.Errorf("%#v", param)
			}
			continue
		}
		if param.mode != 1 || param.value != 2 {
			t.Errorf("%#v", param)
		}
	}
}

func TestReadIntcode(t *testing.T) {
	testData := [][]int{
		{1002, 4, 3, 4, 33},
		{1101, 100, -1, 4, 0},
		{1, 1, 1, 4, 99, 5, 6, 0, 99},
	}
	testAnswers := [][]int{
		{1002, 4, 3, 4, 99},
		{1101, 100, -1, 4, 99},
		{30, 1, 1, 4, 2, 5, 6, 0, 99},
	}
	for i, data := range testData {
		answer := testAnswers[i]
		result := readIntcode(data)
		if len(result) != len(answer) {
			t.Fail()
		} else {
			for j, res := range result {
				if res != answer[j] {
					t.Fail()
				}
			}
		}
	}

}
