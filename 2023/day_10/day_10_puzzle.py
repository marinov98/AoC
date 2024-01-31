def solution(input_file: str) -> None:
    answer, second_answer = solution_helper(input_file)
    print(f"Answer to the problem using {input_file} is:", answer)
    print(f"Answer to the SECOND problem using {input_file} is:", second_answer)


def solution_helper(input_file: str) -> tuple:
    sketch = get_sketch(input_file)
    min_distance, area = find_farthest_distance_from_start(sketch)

    return min_distance, area


def find_farthest_distance_from_start(sketch: list) -> tuple:
    rows = len(sketch)
    columns = len(sketch[0])
    visited = [[-1 for _ in range(columns)] for _ in range(rows)]
    for row in range(rows):
        for col in range(columns):
            if sketch[row][col] == "S":
                true_s = {"|", "-", "J", "L", "7", "F"}
                visited[row][col] = 0
                if row + 1 < rows and sketch[row + 1][col] in "LJ|":
                    find_farthest_distance_iteratively(sketch, row + 1, col, visited)
                    true_s &= {"|", "7", "F"}
                if row - 1 > -1 and sketch[row - 1][col] in "F7|":
                    find_farthest_distance_iteratively(sketch, row - 1, col, visited)
                    true_s &= {"|", "J", "L"}
                if col + 1 < columns and sketch[row][col + 1] in "J-7":
                    find_farthest_distance_iteratively(sketch, row, col + 1, visited)
                    true_s &= {"-", "L", "F"}
                if col - 1 > -1 and sketch[row][col - 1] in "FL-":
                    find_farthest_distance_iteratively(sketch, row, col - 1, visited)
                    true_s &= {"-", "J", "7"}

                assert len(true_s) == 1
                sketch[row][col] = list(true_s)[0]
                break

    # part 2 answer
    ans = 0
    for row in range(rows):
        for col in range(columns):
            if visited[row][col] == -1:
                inverstions = count_inversions(sketch, row, col, visited)
                if inverstions % 2 == 1:
                    ans += 1

    # part 1 answer
    return max(max(row) for row in visited), ans


def find_farthest_distance_iteratively(
    sketch: list, start_row: int, start_col: int, visited: list
) -> None:
    stack = [(start_row, start_col, int(1))]
    rows = len(sketch)
    columns = len(sketch[0])

    while len(stack) != 0:
        row, col, curr_distance = stack.pop()

        if visited[row][col] == -1 or curr_distance < visited[row][col]:
            visited[row][col] = curr_distance
            if sketch[row][col] == "|":
                if row + 1 < rows and sketch[row + 1][col] in "LJ|":
                    stack.append((row + 1, col, curr_distance + 1))
                if row - 1 > -1 and sketch[row - 1][col] in "F7|":
                    stack.append((row - 1, col, curr_distance + 1))
            elif sketch[row][col] == "-":
                if col + 1 < columns and sketch[row][col + 1] in "J-7":
                    stack.append((row, col + 1, curr_distance + 1))
                if col - 1 > -1 and sketch[row][col - 1] in "FL-":
                    stack.append((row, col - 1, curr_distance + 1))
            elif sketch[row][col] == "L":
                if row - 1 > -1 and sketch[row - 1][col] in "F7|":
                    stack.append((row - 1, col, curr_distance + 1))
                if col + 1 < columns and sketch[row][col + 1] in "J-7":
                    stack.append((row, col + 1, curr_distance + 1))
            elif sketch[row][col] == "J":
                if row - 1 > -1 and sketch[row - 1][col] in "F7|":
                    stack.append((row - 1, col, curr_distance + 1))
                if col - 1 > -1 and sketch[row][col - 1] in "FL-":
                    stack.append((row, col - 1, curr_distance + 1))
            elif sketch[row][col] == "7":
                if row + 1 < rows and sketch[row + 1][col] in "LJ|":
                    stack.append((row + 1, col, curr_distance + 1))
                if col - 1 > -1 and sketch[row][col - 1] in "FL-":
                    stack.append((row, col - 1, curr_distance + 1))
            elif sketch[row][col] == "F":
                if row + 1 < rows and sketch[row + 1][col] in "LJ|":
                    stack.append((row + 1, col, curr_distance + 1))
                if col + 1 < columns and sketch[row][col + 1] in "J-7":
                    stack.append((row, col + 1, curr_distance + 1))


def find_farthest_distance_recursively(
    sketch: list, row: int, col: int, curr_distance: int, visited: list
) -> None:
    if visited[row][col] != -1 and curr_distance > visited[row][col]:
        return

    visited[row][col] = curr_distance
    rows = len(sketch)
    columns = len(sketch[0])

    if sketch[row][col] == "|":
        if row + 1 < rows and sketch[row + 1][col] in "LJ|":
            find_farthest_distance_recursively(
                sketch, row + 1, col, curr_distance + 1, visited
            )
        if row - 1 > -1 and sketch[row - 1][col] in "F7|":
            find_farthest_distance_recursively(
                sketch, row - 1, col, curr_distance + 1, visited
            )
    elif sketch[row][col] == "-":
        if col + 1 < columns and sketch[row][col + 1] in "J-7":
            find_farthest_distance_recursively(
                sketch, row, col + 1, curr_distance + 1, visited
            )
        if col - 1 > -1 and sketch[row][col - 1] in "FL-":
            find_farthest_distance_recursively(
                sketch, row, col - 1, curr_distance + 1, visited
            )
    elif sketch[row][col] == "L":
        if row - 1 > -1 and sketch[row - 1][col] in "F7|":
            find_farthest_distance_recursively(
                sketch, row - 1, col, curr_distance + 1, visited
            )
        if col + 1 < columns and sketch[row][col + 1] in "J-7":
            find_farthest_distance_recursively(
                sketch, row, col + 1, curr_distance + 1, visited
            )
    elif sketch[row][col] == "J":
        if row - 1 > -1 and sketch[row - 1][col] in "F7|":
            find_farthest_distance_recursively(
                sketch, row - 1, col, curr_distance + 1, visited
            )
        if col - 1 > -1 and sketch[row][col - 1] in "FL-":
            find_farthest_distance_recursively(
                sketch, row, col - 1, curr_distance + 1, visited
            )
    elif sketch[row][col] == "7":
        if row + 1 < rows and sketch[row + 1][col] in "LJ|":
            find_farthest_distance_recursively(
                sketch, row + 1, col, curr_distance + 1, visited
            )
        if col - 1 > -1 and sketch[row][col - 1] in "FL-":
            find_farthest_distance_recursively(
                sketch, row, col - 1, curr_distance + 1, visited
            )
    elif sketch[row][col] == "F":
        if row + 1 < rows and sketch[row + 1][col] in "LJ|":
            find_farthest_distance_recursively(
                sketch, row + 1, col, curr_distance + 1, visited
            )
        if col + 1 < columns and sketch[row][col + 1] in "J-7":
            find_farthest_distance_recursively(
                sketch, row, col + 1, curr_distance + 1, visited
            )
    return


def get_sketch(input_file: str) -> list:
    sketch = []
    with open(input_file) as file:
        for line in file:
            sketch.append(list(line.strip()))
    return sketch


def count_inversions(sketch, row, end_col, visited):
    # Everything up to (but not including) end_col in the specified row
    count = 0
    for curr_col in range(end_col):
        if visited[row][curr_col] != -1 and sketch[row][curr_col] in "JL|":
            count += 1

    return count


if __name__ == "__main__":
    # solution("test1.txt")
    # solution("test2.txt")
    solution("day_10_puzzle_input.txt")
    # solution("test1_2.txt")
    # solution("test1.5_2.txt")
    # solution("test2_2.txt")
    # solution("test3_2.txt")
