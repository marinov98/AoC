def solution(input_file: str) -> None:
    first_answer = 0
    second_answer = 0
    instances = {}
    card_id = 1
    with open(input_file, "r") as file:
        for line in file:
            first_answer += get_card_points(line.strip())
            second_answer += get_card_points_alt(line.strip(), instances, card_id)

            card_id += 1

    print("Answer to the first puzzle should be:", first_answer)
    print("Answer to the second puzzle should be:", second_answer)


def get_card_points(line: str) -> int:
    card_worth = 0
    first_card_split = line.split(": ")
    numbers_split = first_card_split[1].split(" | ")
    winning_nums_str = numbers_split[0].split(" ")
    our_nums_str = numbers_split[1].split(" ")
    winning_set = {int(win_num) for win_num in winning_nums_str if win_num != ""}
    our_set = {int(our_num) for our_num in our_nums_str if our_num != ""}
    worth_set = winning_set.intersection(our_set)
    if len(worth_set) != 0:
        card_worth = 2 ** (len(worth_set) - 1)

    return card_worth


def get_card_points_alt(line: str, instances: dict, card_id: int) -> int:
    first_card_split = line.split(": ")
    instance_num = 1
    if card_id not in instances:
        instances[card_id] = 1
    numbers_split = first_card_split[1].split(" | ")
    winning_nums_str = numbers_split[0].split(" ")
    our_nums_str = numbers_split[1].split(" ")
    winning_set = {int(win_num) for win_num in winning_nums_str if win_num != ""}
    our_set = {int(our_num) for our_num in our_nums_str if our_num != ""}
    worth_set = winning_set.intersection(our_set)

    for i in range(1, len(worth_set) + 1):
        if card_id + i not in instances:
            instances[card_id + i] = 1

        instances[card_id + i] += instances[card_id]
        instance_num += instances[card_id]

    return instance_num


if __name__ == "__main__":
    solution("day_4_puzzle_input.txt")
