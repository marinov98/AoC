def solution_helper(input_file: str) -> tuple:
    return 0, 0


def solution(files: list[str]) -> None:
    for input_file in files:
        answers = solution_helper(input_file)
        print(f"Solution P1 using '{input_file}': {answers[0]}")
        print(f"Solution P2 using '{input_file}': {answers[1]}")


if __name__ == "__main__":
    solution([
        "test.txt", 
        "day_16_puzzle_input.txt"
    ])

