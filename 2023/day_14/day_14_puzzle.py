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
        [row[:] for row in grid], 1000
    )


def push_rocks(grid: list):
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


def tilt_north(grid: list):
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


def tilt_south(grid: list):
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


def tilt_west(grid: list):
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


def cycle_rocks(grid: list, cycles=10):
    # print("Initial Grid:")
    # print_grid(grid)
    tracker = {}
    total = 0
    for _ in range(cycles):
        total = tilt_north(grid)
        tracker[total] = tracker.get(total, 0) + 1
        total = tilt_west(grid)
        tracker[total] = tracker.get(total, 0) + 1
        total = tilt_south(grid)
        tracker[total] = tracker.get(total, 0) + 1
        total = tilt_east(grid)
        tracker[total] = tracker.get(total, 0) + 1
        # print("\n Cycle:", cycle + 1)
        # print("Last total after cycle", total)
    return total
    # print_grid(grid)
    # print(f"Found {len(tracker)} unique totals after {cycles}")
    # print(tracker)


def push_rock_vertical(grid: list, r, c, invert: bool = False):
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


def push_rock_horizontal(grid: list, r, c, invert: bool = False):
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


if __name__ == "__main__":
    solution("test.txt")
    solution("day_14_puzzle_input.txt")
