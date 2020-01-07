package main

import (
	"container/list"
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strings"
)

type node struct {
	x        int
	y        int
	keys     map[string]int
	distance int
}

func (n *node) String() string {
	keys := make([]string, 0, len(n.keys))
	for k := range n.keys {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	nk := ""
	for _, l := range keys {
		nk += l
	}
	return fmt.Sprintf("%d %d %s", n.x, n.y, nk)
}

func setup(grid string) [][]string {
	ngrid := make([][]string, 0, 4)
	for _, r := range strings.Split(grid, "\n") {
		c := strings.Split(r, "")
		ngrid = append(ngrid, c)
	}
	return ngrid
}

func main() {
	data, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	grid := setup(string(data))
	queue := list.New()
	keys := map[string]int{}
	for y, row := range grid {
		for x, col := range row {
			if "a" <= col && col <= "z" {
				keys[col] = 1
			}
			if col == "@" {
				n := &node{
					x:        x,
					y:        y,
					keys:     make(map[string]int),
					distance: 0,
				}
				queue.PushBack(n)
			}
		}
	}
	fmt.Println(keys)
	fmt.Println(queue.Len())

	visited := make(map[string]int)
	for queue.Len() > 0 {
		// fmt.Println(queue.Len())
		// fmt.Println(visited)
		e := queue.Front()
		n := e.Value.(*node)
		queue.Remove(e)

		// Check to see if visited
		if _, ok := visited[n.String()]; ok {
			// fmt.Printf("Already visited %+v\n", n.String())
			// fmt.Println(queue.Len())
			continue
		}
		visited[n.String()]++

		// Skip out of bounds or walls (#)
		if grid[n.y][n.x] == "#" {
			// fmt.Printf("Out of bounds %+v\n", n)
			continue
		}
		value := grid[n.y][n.x]

		// Skip if reach door and don't have a key
		if "A" <= value && value <= "Z" && n.keys[strings.ToLower(value)] == 0 {
			// fmt.Printf("Reached door %s but dont have a key\n", value)
			continue
		}

		// Copy current keys to new keys
		nk := make(map[string]int)
		for k, v := range n.keys {
			nk[k] = v
		}

		// Add new key to new keys map
		if "a" <= value && value <= "z" {
			nk[value]++
		}

		// Check to see if have all keys and exit if so
		if len(nk) == len(keys) {
			fmt.Println(n)
			fmt.Println(n.distance)
			os.Exit(0)
		}

		// Add to queue
		queue.PushBack(&node{
			x:        n.x + 1,
			y:        n.y,
			keys:     nk,
			distance: n.distance + 1,
		})
		queue.PushBack(&node{
			x:        n.x - 1,
			y:        n.y,
			keys:     nk,
			distance: n.distance + 1,
		})
		queue.PushBack(&node{
			x:        n.x,
			y:        n.y + 1,
			keys:     nk,
			distance: n.distance + 1,
		})
		queue.PushBack(&node{
			x:        n.x,
			y:        n.y - 1,
			keys:     nk,
			distance: n.distance + 1,
		})

	}

}
