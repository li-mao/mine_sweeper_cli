package main

import (
	"fmt"
	"math/rand"
	"strconv"
	"time"
)

func main() {
	length := 10
	width := 10

	r2Map := makeRand2Map(length, length*width)
	mineBase, mineShow := makeMine(length, width, r2Map)

	guess := makeRand2Map(10, length*width)

	// showTable(length, width, mineShow)
	showTable(length, width, mineBase)

	for k := range guess {
		x := k / width
		y := k % width
		fmt.Println("x: ")
		fmt.Println(x)
		fmt.Println("y: ")
		fmt.Println(y)
		gameover := false
		mineShow, gameover = checkMine(x, y, length, width, mineBase, mineShow)
		if gameover {
			fmt.Println("Game Over!!!")
			break
		} else {
			showMineResult(length, width, mineBase, mineShow)
		}
	}

	fmt.Println("hello world")
}

func makeMine(length int, width int, r2Map map[int]int) ([]string, []string) {
	mineBase := make([]string, 0)
	mineShow := make([]string, 0)
	for x := 0; x < length; x++ {
		for y := 0; y < length; y++ {
			// push mineShow
			mineShow = append(mineShow, "-")
			// push mineBase
			index := x*width + y
			if r2Map[index] == 1 {
				mineBase = append(mineBase, "■")
			} else {
				var count int = 0
				if ((x - 1) >= 0) && ((x - 1) < length) && ((y - 1) >= 0) && ((y - 1) < width) && (r2Map[(x-1)*width+(y-1)] == 1) {
					count++
				}
				if ((x - 1) >= 0) && ((x - 1) < length) && ((y) >= 0) && ((y) < width) && (r2Map[(x-1)*width+(y)] == 1) {
					count++
				}
				if ((x - 1) >= 0) && ((x - 1) < length) && ((y + 1) >= 0) && ((y + 1) < width) && (r2Map[(x-1)*width+(y+1)] == 1) {
					count++
				}
				if ((x) >= 0) && ((x) < length) && ((y - 1) >= 0) && ((y - 1) < width) && (r2Map[(x)*width+(y-1)] == 1) {
					count++
				}
				if ((x) >= 0) && ((x) < length) && ((y + 1) >= 0) && ((y + 1) < width) && (r2Map[(x)*width+(y+1)] == 1) {
					count++
				}
				if ((x + 1) >= 0) && ((x + 1) < length) && ((y - 1) >= 0) && ((y - 1) < width) && (r2Map[(x+1)*width+(y-1)] == 1) {
					count++
				}
				if ((x + 1) >= 0) && ((x + 1) < length) && ((y) >= 0) && ((y) < width) && (r2Map[(x+1)*width+(y)] == 1) {
					count++
				}
				if ((x + 1) >= 0) && ((x + 1) < length) && ((y + 1) >= 0) && ((y + 1) < width) && (r2Map[(x+1)*width+(y+1)] == 1) {
					count++
				}

				mineBase = append(mineBase, strconv.Itoa(count))
			}
		}
	}
	return mineBase, mineShow
}

func showTable(length int, width int, data []string) {
	sliceB := make([]string, 0)
	for i := range data {
		sliceB = append(sliceB, data[i])
		if len(sliceB) >= length {
			fmt.Println(sliceB)
			sliceB = sliceB[0:0]
		}
	}
}

func makeRand2Map(count int, max int) map[int]int {
	rand.Seed(time.Now().UnixNano())
	m := make(map[int]int)
	for {
		a := rand.Intn(max)
		m[a] = 1
		if len(m) >= count {
			break
		}
	}
	fmt.Println(m)
	return m
}

func checkMine(x int, y int, length int, width int, mineBase []string, mineShow []string) ([]string, bool) {
	gameover := false
	// checkMap := make(map[int]int)
	result := mineBase[x*width+y]
	mineShow[x*width+y] = "O"
	if result == "■" {
		gameover = true
	} else if result == "0" {
		find0(x, y, length, width, mineBase, mineShow)
	}

	return mineShow, gameover
}

func showMineResult(length int, width int, mineBase []string, mineShow []string) {
	sliceB := make([]string, 0)
	for i := range mineBase {
		result := mineShow[i]
		if mineShow[i] == "O" {
			result = mineBase[i]
		}
		sliceB = append(sliceB, result)
		if len(sliceB) >= length {
			fmt.Println(sliceB)
			sliceB = sliceB[0:0]
		}
	}
}

func find0(x int, y int, length int, width int, mineBase []string, mineShow []string) {
	if ((x - 1) >= 0) && ((x - 1) < length) && ((y - 1) >= 0) && ((y - 1) < width) && (mineShow[(x-1)*width+(y-1)] != "O") && (mineBase[(x-1)*width+(y-1)] == "0") {
		mineShow[(x-1)*width+(y-1)] = "O"
		find0(x-1, y-1, length, width, mineBase, mineShow)
	}
	if ((x - 1) >= 0) && ((x - 1) < length) && ((y) >= 0) && ((y) < width) && (mineShow[(x-1)*width+(y)] != "O") && (mineBase[(x-1)*width+(y)] == "0") {
		mineShow[(x-1)*width+(y)] = "O"
		find0(x-1, y, length, width, mineBase, mineShow)
	}
	if ((x - 1) >= 0) && ((x - 1) < length) && ((y + 1) >= 0) && ((y + 1) < width) && (mineShow[(x-1)*width+(y+1)] != "O") && (mineBase[(x-1)*width+(y+1)] == "0") {
		mineShow[(x-1)*width+(y+1)] = "O"
		find0(x-1, y+1, length, width, mineBase, mineShow)
	}
	if ((x) >= 0) && ((x) < length) && ((y - 1) >= 0) && ((y - 1) < width) && (mineShow[(x)*width+(y-1)] != "O") && (mineBase[(x)*width+(y-1)] == "0") {
		mineShow[(x)*width+(y-1)] = "O"
		find0(x, y-1, length, width, mineBase, mineShow)
	}
	if ((x) >= 0) && ((x) < length) && ((y + 1) >= 0) && ((y + 1) < width) && (mineShow[(x)*width+(y+1)] != "O") && (mineBase[(x)*width+(y+1)] == "0") {
		mineShow[(x)*width+(y+1)] = "O"
		find0(x, y+1, length, width, mineBase, mineShow)
	}
	if ((x + 1) >= 0) && ((x + 1) < length) && ((y - 1) >= 0) && ((y - 1) < width) && (mineShow[(x+1)*width+(y-1)] != "O") && (mineBase[(x+1)*width+(y-1)] == "0") {
		mineShow[(x+1)*width+(y-1)] = "O"
		find0(x+1, y-1, length, width, mineBase, mineShow)
	}
	if ((x + 1) >= 0) && ((x + 1) < length) && ((y) >= 0) && ((y) < width) && (mineShow[(x+1)*width+(y)] != "O") && (mineBase[(x+1)*width+(y)] == "0") {
		mineShow[(x+1)*width+(y)] = "O"
		find0(x+1, y, length, width, mineBase, mineShow)
	}
	if ((x + 1) >= 0) && ((x + 1) < length) && ((y + 1) >= 0) && ((y + 1) < width) && (mineShow[(x+1)*width+(y+1)] != "O") && (mineBase[(x+1)*width+(y+1)] == "0") {
		mineShow[(x+1)*width+(y+1)] = "O"
		find0(x+1, y+1, length, width, mineBase, mineShow)
	}
}
