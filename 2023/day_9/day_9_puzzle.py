def solution(input_file: str) -> None:
    first_answer, second_answer = solution_helper(input_file)

    print(f"First answer using {input_file} should be:", first_answer)
    print(f"Second answer using {input_file} should be:", second_answer)


def solution_helper(input_file: str) -> tuple:
    first_answer = 0
    second_answer = 0
    with open(input_file) as file:
        for line in file:
            curr_answer = expand_sequence(list(map(int, line.strip().split(" "))))
            first_answer += curr_answer[0]
            second_answer += curr_answer[1]

    return first_answer, second_answer


def expand_sequence(start_sequence: list) -> tuple:
    curr_sequence = [num for num in start_sequence]
    sequence_sum = 0
    non_zeroes = 0
    next_sequence = []
    initial_digits = [start_sequence[0]]
    curr_i = 1
    curr = start_sequence[0]
    while True:
        next = curr_sequence[curr_i]
        next_item = next - curr
        next_sequence.append(next_item)
        if next_item != 0:
            non_zeroes += 1
        curr_i += 1
        if curr_i >= len(curr_sequence):
            sequence_sum += next
            if non_zeroes == 0:
                break
            else:
                curr_sequence = [num for num in next_sequence]
                next_sequence = []
                curr_i = 1
                curr = curr_sequence[0]
                initial_digits.append(curr)
                non_zeroes = 0
        else:
            curr = next

    backward_sequence_sum = 0
    while len(initial_digits) > 0:
        backward_sequence_sum = initial_digits.pop() - backward_sequence_sum
    return sequence_sum, backward_sequence_sum


if __name__ == "__main__":
    solution("test.txt")
    solution("day_9_puzzle_input.txt")
