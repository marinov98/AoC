def solution(input_file: str):
    answers = solution_helper(input_file)
    print(f"Solution P1 file '{input_file}': {answers[0]}")
    print(f"Solution P2 file '{input_file}': {answers[1]}")


def print_grid(grid: list):
    for row in grid:
        print(*row, sep="")


def solution_helper(input_file: str):
    grid = []
    with open(input_file, "r") as file:
        for line in file:
            grid.append(list(line.strip()))
    return push_rocks([row[:] for row in grid]), cycle_rocks(
        [row[:] for row in grid], 1000000000
    )


def push_rock_vertical(grid: list, r, c, invert: bool = False) -> int:
    # slide rock as far up north as possible
    curr_row = r - 1 if not invert else r + 1
    limit = -1 if not invert else len(grid)
    offset = -1 if not invert else 1
    while curr_row != limit and grid[curr_row][c] not in "O#":
        curr_row += offset
    curr_row += offset * -1

    # perform push (only if we moved of course)
    if curr_row != r:
        grid[curr_row][c] = "O"
        grid[r][c] = "."
    return curr_row

def push_rock_horizontal(grid: list, r, c, invert: bool = False) -> int:
    curr_col = c - 1 if not invert else c + 1
    limit = -1 if not invert else len(grid[0])
    offset = -1 if not invert else 1
    while curr_col != limit and grid[r][curr_col] not in "O#":
        curr_col += offset

    curr_col += offset * -1
    if curr_col != c:
        grid[r][curr_col] = "O"
        grid[r][c] = "."
    return curr_col


def push_rocks(grid: list) -> int:
    rows = len(grid)
    cols = len(grid[0])
    total_load = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "O":
                curr_row = push_rock_vertical(grid, i, j)

                # calculate load
                total_load += rows - curr_row

    return total_load


def tilt_north(grid: list) -> int:
    rows = len(grid)
    cols = len(grid[0])
    total_load = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "O":
                curr = push_rock_vertical(grid, i, j)

                # calculate load
                total_load += rows - curr
    return total_load


def tilt_south(grid: list) -> int:
    rows = len(grid)
    cols = len(grid[0])
    total_load = 0
    for i in reversed(range(rows)):
        for j in range(cols):
            if grid[i][j] == "O":
                curr = push_rock_vertical(grid, i, j, True)

                # calculate load
                total_load += rows - curr
    return total_load


def tilt_west(grid: list) -> int:
    rows = len(grid)
    cols = len(grid[0])
    total_load = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "O":
                curr = push_rock_horizontal(grid, i, j)

                # calculate load
                total_load += rows - i
    return total_load


def tilt_east(grid: list):
    rows = len(grid)
    cols = len(grid[0])
    total_load = 0
    for i in range(rows):
        for j in reversed(range(cols)):
            if grid[i][j] == "O":
                curr = push_rock_horizontal(grid, i, j, True)

                # calculate load
                total_load += rows - i
    return total_load


def cycle_rocks(grid: list, total_cycles=10) -> int:
    grid_to_insert = tuple([tuple(row[:]) for row in grid])
    grid_tracker = {grid_to_insert}
    grids = [grid_to_insert]
    cycles = 0
    while True:
        cycles += 1
        tilt_north(grid)
        tilt_west(grid)
        tilt_south(grid)
        tilt_east(grid)
        grid_to_insert = tuple([tuple(row[:]) for row in grid])
        if grid_to_insert in grid_tracker:
            break
        grid_tracker.add(grid_to_insert)
        grids.append(grid_to_insert)

    first = grids.index(grid_to_insert)
    target_grid = grids[((total_cycles - first) % (cycles - first)) + first]
    answer = get_load(target_grid)

    return answer

def get_load(grid):
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "O":
                total += len(grid) - i

    return total




if __name__ == "__main__":
    solution("test.txt")
    solution("day_14_puzzle_input.txt")
