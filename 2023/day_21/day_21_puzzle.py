from queue import Queue
from math import floor


def find_steps_inf(start: tuple, grid: list, max_steps: int):
    total_plots = 0
    rows = len(grid)
    cols = len(grid[0])
    q = Queue()
    q.put((start[0], start[1], int(0)))
    visited = {(start[0], start[1], (0, 0))}
    dirs = {"n": (-1, 0), "s": (1, 0), "e": (0, -1), "w": (0, 1)}
    while q.qsize() > 0:
        r, c, curr_steps = q.get()

        if curr_steps % 2 == 0:
            total_plots += 1

        possible_moves = ["n", "s", "e", "w"]

        for move in possible_moves:
            d_r, d_c = dirs[move]
            n_r = r + d_r
            n_c = c + d_c

            curr_id = (floor(n_r // rows), floor(n_c // cols))

            if (
                curr_steps < max_steps
                and (n_r, n_c, curr_id) not in visited
                and grid[n_r % rows][n_c % cols] != "#"
            ):
                visited.add((n_r, n_c, curr_id))
                q.put((n_r, n_c, curr_steps + 1))

    return total_plots


def find_steps(start: tuple, grid: list, max_steps: int):
    total_plots = 0
    rows = len(grid)
    cols = len(grid[0])
    q = Queue()
    q.put((start[0], start[1], int(0)))
    visited = {(start[0], start[1])}
    dirs = {"n": (-1, 0), "s": (1, 0), "e": (0, -1), "w": (0, 1)}
    while q.qsize() > 0:
        r, c, curr_steps = q.get()

        if curr_steps % 2 == 0:
            total_plots += 1

        possible_moves = ["n", "s", "e", "w"]

        for move in possible_moves:
            d_r, d_c = dirs[move]
            n_r = r + d_r
            n_c = c + d_c

            if -1 < n_r < rows and -1 < n_c < cols:
                if (
                    curr_steps < max_steps
                    and (n_r, n_c) not in visited
                    and grid[n_r][n_c] != "#"
                ):
                    visited.add((n_r, n_c))
                    q.put((n_r, n_c, curr_steps + 1))

    return total_plots


def print_grid(grid: list) -> None:
    for row in grid:
        print(*row, sep=" ")


def solution_helper(input_file: str):
    grid = []
    s_r = 0
    s_c = 0
    with open(input_file, "r") as file:
        curr_r = 0
        for line in file:
            line = line.strip()
            if "S" in line:
                s_r = curr_r
                for i, char in enumerate(line):
                    if char == "S":
                        s_c = i
            grid.append(list(line))
            curr_r += 1

    return find_steps((s_r, s_c), grid, 64), find_steps_inf((s_r, s_c), grid, 5000)


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        answers = solution_helper(input_file)
        print(f"Solution P1 using '{input_file}': {answers[0]}")
        print(f"Solution P2 using '{input_file}': {answers[1]}")


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            # "day_21_puzzle_input.txt"
        ]
    )
