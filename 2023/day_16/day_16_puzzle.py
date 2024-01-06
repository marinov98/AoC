def find_energized_tiles(grid: list, alt = False) -> int:
    rows = len(grid)
    cols = len(grid[0])
    if alt: # part 2
        starts = []
        for i in range(rows):
            starts.append((str("r"), i, int(0)))
            starts.append((str("l"), i, cols - 1))
            if i == 0:
                starts.append((str("d"), i, int(0)))
                starts.append((str("d"), i, cols - 1))
            elif i == rows - 1:
                starts.append((str("u"), i, int(0)))
                starts.append((str("u"), i, cols - 1))

        for j in range(1, cols - 1):
            starts.append((str("d"), int(0), j))
            starts.append((str("u"), rows - 1, j))
    else: # part 1
        starts = [(str("r"), int(0), int(0))]

    max_tiles = 0
    while len(starts) != 0:
        beams = [starts.pop()]
        energized_tiles = 0
        visited = set()
        tile_tracker = set()
        while len(beams) != 0:
            d, r, c = beams.pop()
            while -1 < r < rows and -1 < c < cols and (d, r, c) not in visited:
                visited.add((d, r, c))
                if (r, c) not in tile_tracker:
                    energized_tiles += 1
                    tile_tracker.add((r, c))
                if grid[r][c] in "/\\|-":
                    # logic for adding beams and changing directions
                    tile = grid[r][c]
                    if tile == "/":
                        if d == "r":
                            d = "u"
                        elif d == "l":
                            d = "d"
                        elif d == "u":
                            d = "r"
                        elif d == "d":
                            d = "l"
                    elif tile == "\\":
                        if d == "r":
                            d = "d"
                        elif d == "l":
                            d = "u"
                        elif d == "u":
                            d = "l"
                        elif d == "d":
                            d = "r"
                    elif tile == "|":
                        if d == "r" or d == "l":
                            d = "u"
                            beams.append(("d", r + 1, c))
                    elif tile == "-":
                        if d == "u" or d == "d":
                            d = "l"
                            beams.append(("r", r, c + 1))

                if d == "r":
                    c += 1
                elif d == "l":
                    c -= 1
                elif d == "d":
                    r += 1
                elif d == "u":
                    r -= 1
        max_tiles = max(max_tiles, energized_tiles)

    return max_tiles


def solution_helper(input_file: str) -> tuple:
    grid = []
    with open(input_file, "r") as file:
        for line in file:
            grid.append(list(line.strip()))

    # part 1                            # part 2
    return find_energized_tiles(grid), find_energized_tiles(grid, True)


def print_grid(grid: list) -> None:
    for row in grid:
        print(*row, sep=" ")


def solution(input_file: str) -> None:
    answers = solution_helper(input_file)
    print(f"Solution P1 using '{input_file}': {answers[0]}")
    print(f"Solution P2 using '{input_file}': {answers[1]}")


if __name__ == "__main__":
    solution("test.txt")
    solution("day_16_puzzle_input.txt")
