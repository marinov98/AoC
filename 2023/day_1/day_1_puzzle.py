def get_calib_sum(input_file: str) -> None:
    first_answer = 0
    second_answer = 0
    with open(input_file, "r") as file:
        while True:
            next_line = file.readline()

            if not next_line:
                break
            # part 1
            first_answer += get_calib_num(next_line.strip())
            # part 2
            second_answer += get_calib_num_alt(next_line.strip())

    print("Answer to the first puzzle should be:", first_answer)
    print("Answer to the second puzzle should be:", second_answer)


def get_calib_num(input_line: str) -> int:
    begin = 0
    end = len(input_line) - 1
    begin_num = "0"
    end_num = "0"
    while begin <= end:
        if begin_num == "0":
            if input_line[begin].isdigit():
                begin_num = input_line[begin]
            if begin_num == "0":
                begin += 1

        if end_num == "0":
            if input_line[end].isdigit():
                end_num = input_line[end]
            if end_num == "0":
                end -= 1
        if begin_num != "0" and end_num != "0":
            break

    return int(f"{begin_num}{end_num}")


def get_calib_num_alt(input_line: str) -> int:
    print("current word is:", input_line)
    begin = 0
    end = len(input_line) - 1
    begin_num = "0"
    end_num = "0"

    while begin <= end:
        if begin_num == "0":
            if input_line[begin].isdigit():
                begin_num = input_line[begin]
            elif input_line[begin] == "o":
                if input_line[begin : begin + 3] == "one":
                    begin_num = "1"
            elif input_line[begin] == "t":
                if input_line[begin : begin + 3] == "two":
                    begin_num = "2"
                elif input_line[begin : begin + 5] == "three":
                    begin_num = "3"
            elif input_line[begin] == "f":
                if input_line[begin : begin + 4] == "four":
                    begin_num = "4"
                elif input_line[begin : begin + 4] == "five":
                    begin_num = "5"
            elif input_line[begin] == "s":
                if input_line[begin : begin + 3] == "six":
                    begin_num = "6"
                elif input_line[begin : begin + 5] == "seven":
                    begin_num = "7"
            elif input_line[begin] == "e":
                if input_line[begin : begin + 5] == "eight":
                    begin_num = "8"
            elif input_line[begin] == "n":
                if input_line[begin : begin + 4] == "nine":
                    begin_num = "9"
            if begin_num == "0":
                begin += 1

        if end_num == "0":
            if input_line[end].isdigit():
                end_num = input_line[end]
            elif input_line[end] == "e":
                if input_line[end - 2 : end + 1] == "one":
                    end_num = "1"
                elif input_line[end - 4 : end + 1] == "three":
                    end_num = "3"
                elif input_line[end - 3 : end + 1] == "five":
                    end_num = "5"
                elif input_line[end - 3 : end + 1] == "nine":
                    end_num = "9"
            elif input_line[end] == "o":
                if input_line[end - 2 : end + 1] == "two":
                    end_num = "2"
            elif input_line[end] == "r":
                if input_line[end - 3 : end + 1] == "four":
                    end_num = "4"
            elif input_line[end] == "x":
                if input_line[end - 2 : end + 1] == "six":
                    end_num = "6"
            elif input_line[end] == "n":
                if input_line[end - 4 : end + 1] == "seven":
                    end_num = "7"
            elif input_line[end] == "t":
                if input_line[end - 4 : end + 1] == "eight":
                    end_num = "8"
            if end_num == "0":
                end -= 1

        if begin_num != "0" and end_num != "0":
            break
    print(
        f"begin digit: {begin_num} end_digit: {end_num}, final number: {begin_num}{end_num}"
    )
    return int(f"{begin_num}{end_num}")


if __name__ == "__main__":
    get_calib_sum("day_1_puzzle.txt")
