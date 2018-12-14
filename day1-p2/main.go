package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	line := bufio.NewScanner(f)
	numbers := []int{}
	for line.Scan() {
		i, err := strconv.Atoi(line.Text())
		if err != nil {
			log.Fatal(err)
		}
		numbers = append(numbers, i)
	}

	seen := make(map[int]int)
	sum := 0
	for {
		for _, num := range numbers {
			sum += num
			if seen[sum] > 0 {
				fmt.Println(sum)
				return
			}
			seen[sum]++
		}
	}

}
