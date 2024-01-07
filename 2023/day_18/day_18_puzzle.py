def solution_helper(input_file: str) -> tuple:
    return 0, 0

def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        solution_helper(input_file)

if __name__ == "__main__":
    solution([
        "test.txt"
        # "day_18_puzzle_input.txt"
    ])
