def solution(input_file: str) -> None:
    print(f"Answer to the first problem using file '{input_file}' is: {solution_helper(input_file)}")
    print(f"Answer to the second problem using file '{input_file}' is: {solution_helper(input_file, True)}")


def solution_helper(input_file: str, alt: bool = False) -> int:
    total = 0
    with open(input_file, "r") as f:
        for line in f:
            curr = line.strip().split(" ")
            formatted_springs = tuple(map(int, curr[1].split(",")))
            spring_cfg = curr[0]
            if alt:
                spring_cfg = "?".join([spring_cfg] * 5)
                formatted_springs *= 5
                
            total += get_count(spring_cfg, formatted_springs, {})
    return total


def get_count(spring_cfg, spring_nums, cache: dict) -> int:
    if spring_cfg == "":
        return 1 if spring_nums == () else 0

    if spring_nums == ():
        return 0 if "#" in spring_cfg else 1

    key = (spring_cfg, spring_nums)
    if key in cache:
        return cache[key]

    result = 0
    if spring_cfg[0] == "." or spring_cfg[0] == "?":
        result += get_count(spring_cfg[1:], spring_nums, cache)

    if spring_cfg[0] == "#" or spring_cfg[0] == "?":
        if (spring_nums[0] <= len(spring_cfg)) and ("." not in spring_cfg[:spring_nums[0]]) and (spring_nums[0] == len(spring_cfg) or spring_cfg[spring_nums[0]] != "#"):
            result += get_count(spring_cfg[spring_nums[0] + 1:], spring_nums[1:], cache)

    cache[key] = result
    return result


if __name__ == "__main__":
    solution("day_12_puzzle_input.txt")
