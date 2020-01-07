package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type deck struct {
	cards []int
}

func (d *deck) newStack() {
	stack := make([]int, 0, len(d.cards))
	for i := len(d.cards) - 1; i >= 0; i-- {
		stack = append(stack, d.cards[i])
	}
	d.cards = stack
}

func modLikePython(d, m int) int {
	var res int = d % m
	if (res < 0 && m > 0) || (res > 0 && m < 0) {
		return res + m
	}
	return res
}

func (d *deck) cut(n int) {
	var stack []int
	pos := modLikePython(n, len(d.cards))
	stack = d.cards[pos:]
	stack = append(stack, d.cards[:pos]...)
	d.cards = stack
}

func (d *deck) increment(n int) {
	stack := make([]int, len(d.cards))
	stack[0] = d.cards[0]
	start := 0
	for i := 1; i < len(d.cards); i++ {
		pos := modLikePython((n + start), len(d.cards))
		stack[pos] = d.cards[i]
		start = pos
	}
	d.cards = stack
}

func new(i int) *deck {
	cards := make([]int, i)
	for j := 0; j < i; j++ {
		cards[j] = j
	}
	return &deck{cards: cards}
}

func setup(filename string) []string {
	s, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.Split(string(s), "\n")
}

var times = 101741582076661

func main() {
	instructions := setup("input.txt")
	test := new(119315717514047)
	for i := 0; i < times-1; i++ {
		for _, ins := range instructions {
			if strings.Contains(ins, "stack") {
				test.newStack()
				continue
			}
			apart := strings.Split(ins, " ")
			mov, _ := strconv.Atoi(apart[len(apart)-1])
			if strings.Contains(ins, "cut") {
				test.cut(mov)
			} else if strings.Contains(ins, "increment") {
				test.increment(mov)
			}
		}
	}
	for i, card := range test.cards {
		if card == 2019 {
			fmt.Println(i)
		}
	}
}
