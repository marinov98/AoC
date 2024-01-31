def solution(input_file: str) -> None:
    first_answer = 1
    second_answer = 0
    inputs = open(input_file, "r").read().split("\n")
    inputs.pop()  # remove last line
    parameters = get_parameters(inputs)
    for t, d in parameters:
        first_answer *= get_ways(t, d)

    big_t, big_d = get_parameters_alt(inputs)
    print(f"\nbig t {big_t} big d {big_d}")
    second_answer += get_ways(big_t, big_d)

    print("Answer to the first puzzle should be:", first_answer)
    print("\nAnswer to the second puzzle should be:", second_answer)


def get_parameters(inputs: list) -> list[tuple]:
    t = []
    res = []
    for input in inputs:
        test_split = input.split(":")
        if "Time" in test_split[0]:
            for input_str in test_split[1].strip().split(" "):
                if input_str.isdigit():
                    t.append(int(input_str))
        else:
            time_index = 0
            for input_str in test_split[1].strip().split(" "):
                if input_str.isdigit():
                    res.append((t[time_index], int(input_str)))
                    time_index += 1

    return res


def get_parameters_alt(inputs: list) -> tuple:
    t = []
    res = []
    d_res = 0
    t_res = 0
    for input in inputs:
        test_split = input.split(":")
        if "Time" in test_split[0]:
            for input_str in test_split[1].strip().split(" "):
                if input_str.isdigit():
                    t.append(input_str)
        else:
            for input_str in test_split[1].strip().split(" "):
                if input_str.isdigit():
                    res.append(input_str)

    t_res = int("".join(t))
    d_res = int("".join(res))
    return (t_res, d_res)


def get_ways(t: int, d: int) -> int:
    ways = 0
    if t == 0 or d == 0:
        return 0

    last_res = 0
    for seconds_held in range(1, t):
        curr_res = (t - seconds_held) * seconds_held
        if curr_res > d:
            ways += 1
        elif curr_res < last_res:
            print(f"on {seconds_held} there was no need to continue!")
            break
        last_res = curr_res

    return ways


if __name__ == "__main__":
    solution("test.txt")
    solution("day_6_puzzle_input.txt")
