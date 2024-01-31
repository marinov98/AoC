def solution(input_file: str) -> None:
    first_answer = 0
    second_answer = 0
    engine_schematic = []
    with open(input_file, "r") as file:
        for line in file:
            engine_schematic.append(list(line.strip()))

        first_answer = find_part_numbers(engine_schematic)
        second_answer = find_gear_ratio(engine_schematic)

    print("Answer to the first puzzle should be:", first_answer)
    print("Answer to the second puzzle should be:", second_answer)


def find_part_numbers(engine_schematic: str) -> list:
    symbol_set = {"*", "+", "#", "$", "/", "&", "!", "-", "_", "^", "%", "@", "="}
    rows = len(engine_schematic)
    columns = len(engine_schematic[0])
    visited = [[False for _ in range(columns)] for _ in range(rows)]
    part_num_sum = 0
    for row in range(rows):
        for col in range(columns):
            if engine_schematic[row][col].isdigit() and not visited[row][col]:
                num_str = ""
                symbol_found = False
                curr_row = row
                curr_col = col
                while (
                    engine_schematic[curr_row][curr_col]
                    and engine_schematic[curr_row][curr_col].isdigit()
                ):
                    visited[curr_row][curr_col] = True
                    num_str += engine_schematic[curr_row][curr_col]
                    if symbol_found == False:
                        if (
                            curr_col + 1 < columns
                            and engine_schematic[curr_row][curr_col + 1] in symbol_set
                        ):  # right
                            symbol_found = True
                        if (
                            curr_col - 1 > -1
                            and engine_schematic[curr_row][curr_col - 1] in symbol_set
                        ):  # left
                            symbol_found = True
                        if (
                            curr_row + 1 < rows
                            and engine_schematic[curr_row + 1][curr_col] in symbol_set
                        ):  # below
                            symbol_found = True
                        if (
                            curr_row - 1 > -1
                            and engine_schematic[curr_row - 1][curr_col] in symbol_set
                        ):  # above
                            symbol_found = True
                        if (
                            curr_row + 1 < rows
                            and curr_col - 1 > -1
                            and engine_schematic[curr_row + 1][curr_col - 1]
                            in symbol_set
                        ):  # diagonals
                            symbol_found = True
                        if (
                            curr_row - 1 > -1
                            and curr_col - 1 > -1
                            and engine_schematic[curr_row - 1][curr_col - 1]
                            in symbol_set
                        ):  # diagonals
                            symbol_found = True
                        if (
                            curr_row - 1 > -1
                            and curr_col + 1 < columns
                            and engine_schematic[curr_row - 1][curr_col + 1]
                            in symbol_set
                        ):  # diagonals
                            symbol_found = True
                        if (
                            curr_row + 1 < rows
                            and curr_col + 1 < columns
                            and engine_schematic[curr_row + 1][curr_col + 1]
                            in symbol_set
                        ):  # diagonals
                            symbol_found = True
                    if curr_col == columns - 1:
                        break
                    curr_col += 1
                if symbol_found:
                    part_num_sum += int(num_str)

    return part_num_sum


def find_gear_ratio(engine_schematic: str) -> int:
    rows = len(engine_schematic)
    columns = len(engine_schematic[0])
    visited = [[False for _ in range(columns)] for _ in range(rows)]
    gear_ratio_sum = 0
    for row in range(rows):
        for col in range(columns):
            if engine_schematic[row][col] == "*" and not visited[row][col]:
                num_found = 0
                curr_row = row
                curr_col = col
                gear = []
                visited[curr_row][curr_col] = True
                if (
                    not visited[curr_row][curr_col + 1]
                    and curr_col + 1 < columns
                    and engine_schematic[curr_row][curr_col + 1].isdigit()
                ):  # right
                    num_found += 1
                    if num_found > 2:
                        break
                    gear.append(
                        extract_adjacent_number(
                            engine_schematic, visited, curr_row, curr_col + 1
                        )
                    )

                if (
                    not visited[curr_row][curr_col - 1]
                    and curr_col - 1 > -1
                    and engine_schematic[curr_row][curr_col - 1].isdigit()
                ):  # left
                    num_found += 1
                    if num_found > 2:
                        break
                    extracted_num = extract_adjacent_number(
                        engine_schematic, visited, curr_row, curr_col - 1
                    )
                    if extracted_num != 0:
                        gear.append(extracted_num)
                if (
                    not visited[curr_row + 1][curr_col]
                    and curr_row + 1 < rows
                    and engine_schematic[curr_row + 1][curr_col].isdigit()
                ):  # below
                    num_found += 1
                    if num_found > 2:
                        break
                    extracted_num = extract_adjacent_number(
                        engine_schematic, visited, curr_row + 1, curr_col
                    )
                    if extracted_num != 0:
                        gear.append(extracted_num)
                if (
                    not visited[curr_row - 1][curr_col]
                    and curr_row - 1 > -1
                    and engine_schematic[curr_row - 1][curr_col].isdigit()
                ):  # above
                    num_found += 1
                    if num_found > 2:
                        break
                    extracted_num = extract_adjacent_number(
                        engine_schematic, visited, curr_row - 1, curr_col
                    )
                    if extracted_num != 0:
                        gear.append(extracted_num)
                if (
                    not visited[curr_row + 1][curr_col - 1]
                    and curr_row + 1 < rows
                    and curr_col - 1 > -1
                    and engine_schematic[curr_row + 1][curr_col - 1].isdigit()
                ):  # diagonals
                    num_found += 1
                    if num_found > 2:
                        break
                    extracted_num = extract_adjacent_number(
                        engine_schematic, visited, curr_row + 1, curr_col - 1
                    )
                    if extracted_num != 0:
                        gear.append(extracted_num)
                if (
                    not visited[curr_row - 1][curr_col - 1]
                    and curr_row - 1 > -1
                    and curr_col - 1 > -1
                    and engine_schematic[curr_row - 1][curr_col - 1].isdigit()
                ):  # diagonals
                    num_found += 1
                    if num_found > 2:
                        break
                    extracted_num = extract_adjacent_number(
                        engine_schematic, visited, curr_row - 1, curr_col - 1
                    )
                    if extracted_num != 0:
                        gear.append(extracted_num)
                if (
                    not visited[curr_row - 1][curr_col + 1]
                    and curr_row - 1 > -1
                    and curr_col + 1 < columns
                    and engine_schematic[curr_row - 1][curr_col + 1].isdigit()
                ):  # diagonals
                    num_found += 1
                    if num_found > 2:
                        break
                    extracted_num = extract_adjacent_number(
                        engine_schematic, visited, curr_row - 1, curr_col + 1
                    )
                    if extracted_num != 0:
                        gear.append(extracted_num)
                if (
                    not visited[curr_row + 1][curr_col + 1]
                    and curr_row + 1 < rows
                    and curr_col + 1 < columns
                    and engine_schematic[curr_row + 1][curr_col + 1].isdigit()
                ):  # diagonals
                    num_found += 1
                    if num_found > 2:
                        break
                    extracted_num = extract_adjacent_number(
                        engine_schematic, visited, curr_row + 1, curr_col + 1
                    )
                    if extracted_num != 0:
                        gear.append(extracted_num)
                print("gear", gear)
                print("number found", num_found)
                if num_found == 2:
                    gear_ratio_sum += gear[0] * gear[1]

    return gear_ratio_sum


def extract_adjacent_number(
    engine_schematics: str, visited: list[list[bool]], row: int, col: int
) -> int:
    if visited[row][col] == True:
        return 0

    visited[row][col] = True
    while col > -1 and engine_schematics[row][col].isdigit():
        col -= 1

    col += 1
    num_arr = []
    while col < len(engine_schematics[0]) and engine_schematics[row][col].isdigit():
        visited[row][col] = True
        num_arr.append(engine_schematics[row][col])
        col += 1
    return int("".join(num_arr))


if __name__ == "__main__":
    solution("day_3_puzzle_input.txt")
