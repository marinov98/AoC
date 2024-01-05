def find_energized_tiles(grid: list) -> int:
    energized_tiles = 0
    beams = [(str("r"), int(0), int(0))]
    visited = set()
    tile_tracker = set()
    rows = len(grid)
    cols = len(grid[0])
    while len(beams) != 0:
        d, r, c = beams.pop()
        while -1 < r < rows and -1 < c < cols and (d, r, c) not in visited:
            # print(f"row: {r} col: {c} elem: {grid[r][c]} beams: {beams}")
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

    return energized_tiles


def solution_helper(input_file: str) -> tuple:
    grid = []
    with open(input_file, "r") as file:
        for line in file:
            grid.append(list(line.strip()))

    # part 1
    return find_energized_tiles(grid), 0



def print_grid(grid: list) -> None:
    for row in grid:
        print(*row, sep=" ")


def solution(input_file: str) -> None:
    answers = solution_helper(input_file)
    print(f"Solution P1 using '{input_file}': {answers[0]}")
    # print(f"Solution P2 using '{input_file}': {answers[1]}")

if __name__ == "__main__":
    solution("test.txt")
    solution("day_16_puzzle_input.txt")
