def solution(input_file: str) -> None:
    final_res = solution_helper(input_file)
    print(f"Answer P1 using '{input_file}' :", final_res[0])
    print(f"Answer P2 using '{input_file}' :", final_res[1])


def solution_helper(input_file: str) -> tuple:
    input = []
    curr_pattern = []
    with open(input_file, "r") as f:
        for line in f:
            if "." in line or "#" in line:
                curr_pattern.append(line.strip())
            else:
                input.append(curr_pattern)
                curr_pattern = []
    input.append(curr_pattern)
    return find_mirrors(input)


def find_mirrors(input: list) -> tuple:
    answer = 0
    answer_2 = 0
    for pattern in input:
        res, smudges = find_mirrors_in_pattern(pattern)
        answer += res
        target = smudges[0][3][0] + 1
        answer_2 += (target * 100) if smudges[0][0] == "r" else target

    return answer, answer_2


def find_mirrors_in_pattern(pattern: list) -> tuple:
    rows = len(pattern)
    cols = len(pattern[0])
    mirrors = []
    answer = 0

    potential_smudges = []
    # vertical mirrors
    for j in range(cols - 1):
        if is_mirror_col(j, j + 1, pattern, potential_smudges):
            mirrors.append((j + 1, j + 2, "c"))  # match numbers with problem
            answer += j + 1

    # horizontal mirrors
    for i in range(rows - 1):
        if is_mirror_row(i, i + 1, pattern, potential_smudges):
            mirrors.append((i + 1, i + 2, "r"))  # match numbers with problem
            answer += (i + 1) * 100

    return answer, potential_smudges


def is_mirror_row(r1, r2, pattern: list, potential_smudges: list) -> bool:
    rows = len(pattern)
    cols = len(pattern[0])
    is_mirror = True
    curr_faults = []
    for j in range(cols):
        l, r = r1, r2
        while l > -1 and r < rows:
            if pattern[l][j] != pattern[r][j]:
                curr_faults.append(("r", l, j, (r1, r2)))
                is_mirror = False
            l -= 1
            r += 1
    if len(curr_faults) == 1:
        potential_smudges.append(curr_faults[0])

    return is_mirror


def is_mirror_col(c1, c2, pattern: list, potential_smudges: list) -> bool:
    cols = len(pattern[0])
    rows = len(pattern)
    curr_faults = []
    is_mirror = True
    for i in range(rows):
        l, r = c1, c2
        while l > -1 and r < cols:
            if pattern[i][l] != pattern[i][r]:
                curr_faults.append(("c", i, l, (c1, c2)))
                is_mirror = False
            l -= 1
            r += 1
    if len(curr_faults) == 1:
        potential_smudges.append(curr_faults[0])
    return is_mirror


if __name__ == "__main__":
    solution("test.txt")
    solution("day_13_puzzle_input.txt")
