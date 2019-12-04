package main

import (
	"fmt"
	"strconv"
)

func acceptable(code string) bool {
	hasDouble := false
	for i := 0; i < len(code); i++ {
		if i == len(code)-1 {
			continue
		}
		current, _ := strconv.Atoi(string(code[i]))
		next, _ := strconv.Atoi(string(code[i+1]))
		if current > next {
			return false
		} else if current == next {
			hasDouble = true
		}
	}
	if hasDouble {
		return doubleChecker(code)
	}
	return false
}

func doubleChecker(code string) bool {
	cnt := make(map[string]int)
	for _, x := range code {
		cnt[string(x)]++
	}
	hasDouble := false
	for _, v := range cnt {
		if v == 2 {
			hasDouble = true
			break
		}
	}
	return hasDouble
}

func main() {
	total := 0
	start := 231832
	end := 767346
	for i := start; i < end; i++ {
		si := strconv.Itoa(i)
		if acceptable(si) {
			total++
		}
	}
	fmt.Println(total)
}
