def solution(input_file: str) -> None:
    answers = solution_helper(input_file)
    print(f"Solution P1 using '{input_file}': {answers[0]}")
    print(f"Solution P2 using '{input_file}': {answers[1]}")


def solution_helper(input_file: str) -> tuple:
    sequence = []
    with open(input_file, "r") as file:
        for line in file:
            sequence = line.strip().split(",")

    return handle_sequence(sequence)


def handle_sequence(sequence: list) -> tuple:
    total = 0
    tracker = [[] for _ in range(256)]
    focal_len_tracker = {}
    for curr_str in sequence:
        total += run_hash_alg(curr_str)
        run_hashmap_alg(curr_str, tracker, focal_len_tracker)

    total_2 = calculate_focusing_power(tracker, focal_len_tracker)

    return total, total_2


def run_hash_alg(string: str) -> int:
    value = 0
    for char in string:
        if char != "\n":
            value += ord(char)
            value *= 17
            value %= 256

    return value


def run_hashmap_alg(string: str, tracker, focal_len_tracker):
    operation_type = 0  # 0 for - 1 for =
    key_to_check = None
    focal_len = -1
    if "=" in string:
        operation_type = 1
        temp_tuple = string.strip().split("=")
        key_to_check = temp_tuple[0]
        focal_len = int(temp_tuple[1])
    else:
        key_to_check = string.strip().split("-")[0]

    box_key = run_hash_alg(key_to_check)
    id = (key_to_check, box_key)
    if operation_type == 1:  # =
        if id not in focal_len_tracker:
            tracker[box_key].append(key_to_check)
        if focal_len != -1:
            focal_len_tracker[id] = focal_len
    else:  # -
        if id in focal_len_tracker:
            tracker[box_key].remove(key_to_check)
            del focal_len_tracker[id]


def calculate_focusing_power(tracker, focal_len_tracker):
    total = 0
    for i, box in enumerate(tracker):
        for j, key_to_check in enumerate(box):
            id = (key_to_check, i)
            total += (i + 1) * (j + 1) * focal_len_tracker[id]

    return total


if __name__ == "__main__":
    solution("test.txt")
    solution("day_15_puzzle_input.txt")
    # print(run_hash_alg("rn"))
