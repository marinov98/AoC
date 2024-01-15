def print_grid(grid: list[list]) -> None:
    for row in grid:
        print(*row, sep=" ")

def solution_helper(input_file: str):
    grid = []
    with open(input_file, "r") as file:
        for line in file:
            grid.append(list(line.strip()))

    print_grid(grid)
    return 0


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        solution_helper(input_file)

if __name__ == "__main__":
    solution([
        "test.txt",
        # "day_23_puzzle_input.txt"
    ])
