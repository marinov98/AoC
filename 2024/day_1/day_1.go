package day1

import (
	"bufio"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

func readFile(fileName string) ([]int, []int) {
	f, err := os.Open(fileName)

	if err != nil {
		log.Fatal(err)
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)
	leftSlice := []int{}
	rightSlice := []int{}

	for scanner.Scan() {
		currLine := strings.Split(scanner.Text(), "   ")
		if currLine[0] != "" && currLine[1] != "" {
			leftNum, err := strconv.Atoi(currLine[0])
			if err != nil {
				log.Fatal(err)
			}

			rightNum, err := strconv.Atoi(currLine[1])
			if err != nil {
				log.Fatal(err)
			}

			leftSlice = append(leftSlice, leftNum)
			rightSlice = append(rightSlice, rightNum)

		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return leftSlice, rightSlice

}

func handle_input(leftSlice []int, rightSlice []int) int {
	sort.Slice(leftSlice, func(i, j int) bool {
		return leftSlice[i] < leftSlice[j]
	})

	sort.Slice(rightSlice, func(i, j int) bool {
		return rightSlice[i] < rightSlice[j]
	})

	var sum int
	for i := range leftSlice {
		sum += (int(math.Abs(float64(leftSlice[i]) - float64(rightSlice[i]))))
	}

	return sum
}

func handle_input_2(leftSlice []int, rightSlice []int) int {
	var tracker map[int]int = make(map[int]int)
	var sum int

	for _, ele := range rightSlice {
		count, ok := tracker[ele]
		if ok {
			tracker[ele] = count + 1
		} else {
			tracker[ele] = 1
		}
	}

	for _, ele := range leftSlice {
		count, ok := tracker[ele]
		if ok {
			sum += (ele * count)
		}
	}

	return sum
}
