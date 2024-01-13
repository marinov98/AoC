def find_steps(start: tuple, grid: list):
    print(f"{start[0]} {start[1]} have an S!")
    print_grid(grid)
    return 0

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

    return find_steps((s_r, s_c),grid)


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        answers = solution_helper(input_file)
        print(f"Solution P1 using '{input_file}': {answers}")


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            # "day_21_puzzle_input.txt"
        ]
    )
