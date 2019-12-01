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
	sum := 0
	for line.Scan() {
		i, err := strconv.Atoi(line.Text())
		if err != nil {
			log.Fatal(err)
		}
		sum += i
	}
	fmt.Println(sum)

}
