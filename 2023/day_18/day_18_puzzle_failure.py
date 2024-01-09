def calculate_inside_area(painted_grid: list):
    new_total = 0
    for i in range(len(painted_grid)):
        for j in range(len(painted_grid[0])):
            if painted_grid[i][j] == ".":
                new_total += check_if_inside(j, painted_grid[i])

    return new_total

def check_if_inside(c: int, grid_row: list) -> int:
    curr = c - 1
    passes = 0
    while curr > -1:
        if grid_row[curr] == "#":
            while curr > -1 and grid_row[curr] == "#":
                curr -= 1
            passes += 1
        else:
            curr -= 1

    return 0 if passes % 2 == 0 else 1

def paint_grid(
    grid: list,
    instructions: list[tuple],
    reverse_r: bool = False,
    reverse_c: bool = False,
):
    r = 0 if not reverse_r else len(grid) - 1
    c = 0 if reverse_c else len(grid[0]) - 1
    print(f"starting r: {r} starts c: {c}")
    grid[r][c] = "#"  # initial dig

    total = 0
    dirs = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    for dir, steps in instructions:
        r_offset, c_offset = dirs[dir]
        print(f"Direction: {dir}, Steps: {steps}, row: {r} col: {c}")
        for _ in range(steps):
            r += r_offset
            c += c_offset
            grid[r][c] = "#"
            total += 1
    return total + calculate_inside_area(grid)


def solution_helper(input_file: str) -> tuple:
    tracker = {}
    rows = -1
    curr_r = 1
    curr_c = 1
    cols = -1
    instructions = []
    reverse_r = False
    reverse_c = False
    dirs_found = set()
    with open(input_file, "r") as file:
        for line in file:
            item = line.strip().split(" ")
            dir = item[0]
            steps = int(item[1])
            instructions.append((dir, steps))
            if dir in "RL":
                if dir not in dirs_found:
                    if not reverse_c and dir == "L" and "R" not in dirs_found:
                        reverse_c = True
                    dirs_found.add(dir)
                if dir == "R":
                    curr_c = abs(curr_c + steps)
                else:
                    curr_c = abs(curr_c - steps)

                cols = max(cols, curr_c)
            elif dir in "UD":
                if dir not in dirs_found:
                    if not reverse_r and dir == "U" and "D" not in dirs_found:
                        reverse_r = True
                    dirs_found.add(dir)
                if dir == "D":
                    curr_r = abs(curr_r + steps)
                else:
                    curr_r = abs(curr_r - steps)

                rows = max(rows, curr_r)

            tracker[item[2]] = (item[0], steps)
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    # print_grid(grid)
    print(paint_grid(grid, instructions, reverse_r, reverse_c))

    return 0, 0


def print_grid(grid: list) -> None:
    for row in grid:
        print(*row, sep=" ")


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        solution_helper(input_file)


if __name__ == "__main__":
    solution(
        [
            # "test.txt"
            "day_18_puzzle_input.txt"
        ]
    )
