package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {
	f, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	line := bufio.NewScanner(f)
	var twos, threes int
	for line.Scan() {
		word := line.Text()
		letters := make(map[rune]int)
		for _, i := range word {
			letters[i]++
		}
		var istwo, isthree bool
		for _, j := range letters {
			if j == 2 && istwo == false {
				twos++
				istwo = true
			} else if j == 3 && isthree == false {
				threes++
				isthree = true
			}
		}
	}
	fmt.Println(twos * threes)
}
