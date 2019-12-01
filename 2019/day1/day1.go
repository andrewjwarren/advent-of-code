package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func calculateFuel(mass int) int {
	fuel := (mass / 3) - 2
	if fuel <= 0 {
		fuel = 0
	}
	return fuel
}

func totalFuel(mass int) int {
	fuelNeeded := 0
	for mass > 0 {
		mass = calculateFuel(mass)
		fuelNeeded += mass
	}
	return fuelNeeded
}

func main() {
	dat, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	total := 0
	for _, mass := range strings.Split(string(dat), "\n") {
		input, err := strconv.Atoi(mass)
		if err != nil {
			continue
		}
		total += totalFuel(input)
	}
	fmt.Println(total)
}
