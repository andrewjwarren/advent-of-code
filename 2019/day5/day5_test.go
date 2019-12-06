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
