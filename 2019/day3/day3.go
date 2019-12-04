package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type wire struct {
	coordinates map[coordinate]int
	counter     int
	position    coordinate
}

type coordinate struct {
	x     int
	y     int
	steps int
}

func (w *wire) up(spaces int) {
	x := w.position.x
	y := w.position.y
	for i := 0; i < spaces; i++ {
		y++
		w.update(x, y)
	}
}

func (w *wire) down(spaces int) {
	x := w.position.x
	y := w.position.y
	for i := 0; i < spaces; i++ {
		y--
		w.update(x, y)
	}
}

func (w *wire) left(spaces int) {
	x := w.position.x
	y := w.position.y
	for i := 0; i < spaces; i++ {
		x--
		w.update(x, y)
	}
}

func (w *wire) right(spaces int) {
	x := w.position.x
	y := w.position.y
	for i := 0; i < spaces; i++ {
		x++
		w.update(x, y)
	}
}

func (w *wire) update(x, y int) {
	w.counter++
	c := newCoordinate(x, y)
	w.position = c
	if _, ok := w.coordinates[c]; ok {
		return
	}
	w.coordinates[c] = w.counter
}

func (w *wire) move(instructions string) {
	dMap := map[string]func(int){
		"R": w.right,
		"L": w.left,
		"U": w.up,
		"D": w.down,
	}
	for _, i := range strings.Split(instructions, ",") {
		direction, spaces := parseInstruction(i)
		dMap[direction](spaces)
	}
}

func findIntersections(w1, w2 wire) []coordinate {
	cords := make([]coordinate, 0, len(w1.coordinates)/2)
	for k, v := range w1.coordinates {
		if value, ok := w2.coordinates[k]; ok {
			c := newCoordinate(k.x, k.y)
			c.steps = v + value
			cords = append(cords, c)
		}
	}
	return cords
}

func newCoordinate(x, y int) coordinate {
	return coordinate{
		x: x,
		y: y,
	}
}

func new() *wire {
	start := newCoordinate(0, 0)
	c := make(map[coordinate]int)
	w := wire{
		counter:     0,
		position:    start,
		coordinates: c,
	}
	return &w
}

func parseInstruction(instruction string) (string, int) {
	direction := string(instruction[0])
	spaces, err := strconv.Atoi(instruction[1:])
	if err != nil {
		return "", 0
	}
	return direction, spaces
}

func fewestSteps(c []coordinate) int {
	fewest := 0
	for i, cord := range c {
		if i == 0 {
			fewest = cord.steps
			continue
		}
		if cord.steps < fewest {
			fewest = cord.steps
		}
	}
	return fewest
}

func main() {
	data, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	wire1 := new()
	wire1.move(strings.Split(string(data), "\n")[0])
	wire2 := new()
	wire2.move(strings.Split(string(data), "\n")[1])
	intersections := findIntersections((*wire1), (*wire2))
	fmt.Println(fewestSteps(intersections))
}
