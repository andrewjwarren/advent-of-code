package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"os"
	"strings"
)

func compareWords(a, b string) (string, error) {
	diff := 0
	var letters strings.Builder
	for i := range a {
		if a[i] != b[i] {
			diff++
			continue
		}
		letters.WriteByte(a[i])
	}
	if diff > 1 {
		return "", errors.New("Nope")
	}
	return letters.String(), nil
}

func main() {
	f, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	line := bufio.NewScanner(f)
	words := []string{}
	for line.Scan() {
		word := line.Text()
		words = append(words, word)
	}
	for i, a := range words {
		// Check to make sure there is a next word
		if i+1 == len(words) {
			continue
		}

		for _, b := range words[i+1:] {
			var common string
			common, err := compareWords(a, b)
			if err != nil {
				continue
			}
			fmt.Println(common)
		}
	}
}
