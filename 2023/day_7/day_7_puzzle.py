def solution(input_file: str) -> None:
    rank_map = {}
    bid_map = {}
    rank_map_alt = {}
    bid_map_alt = {}
    with open(input_file) as file:
        for line in file:
            rank_map, bid_map = fill_maps(rank_map, bid_map, line.strip())
            rank_map_alt, bid_map_alt = fill_maps_alt(rank_map_alt, bid_map_alt, line.strip())
    print("Answer to the first question should be:", get_winnings(rank_map, bid_map))
    print("Answer to the second question should be:", get_winnings(rank_map_alt, bid_map_alt, alt=True))


def fill_maps(rank_map: dict, bid_map: dict, input_line: str) -> tuple:
    card_split = input_line.split()
    cards = card_split[0]
    bid_map[cards] = int(card_split[1])
    symbol_map = {}
    for card in cards:
        symbol_map[card] = symbol_map.get(card, 0) + 1

    if len(symbol_map) == len(cards):  # all cards are distinct
        if "High card" not in rank_map:
            rank_map["High card"] = [cards]
        else:
            rank_map["High card"].append(cards)
    elif len(symbol_map) == 4:  # one pair
        if "One pair" not in rank_map:
            rank_map["One pair"] = [cards]
        else:
            rank_map["One pair"].append(cards)
    elif len(symbol_map) == 3:  # two pair or 3 of a kind
        for val in symbol_map.values():
            if val != 1:
                if val == 2:
                    if "Two pair" not in rank_map:
                        rank_map["Two pair"] = [cards]
                    else:
                        rank_map["Two pair"].append(cards)
                else:
                    if "Three of a kind" not in rank_map:
                        rank_map["Three of a kind"] = [cards]
                    else:
                        rank_map["Three of a kind"].append(cards)
                break
    elif len(symbol_map) == 2:  # four of a kind or full house
        for val in symbol_map.values():
            if val == 4 or val == 1:  # four of a kind case
                if "Four of a kind" not in rank_map:
                    rank_map["Four of a kind"] = [cards]
                else:
                    rank_map["Four of a kind"].append(cards)
            else:  # full house case
                if "Full house" not in rank_map:
                    rank_map["Full house"] = [cards]
                else:
                    rank_map["Full house"].append(cards)
            break
    elif len(symbol_map) == 1:  # Five of a kind
        if "Five of a kind" not in rank_map:
            rank_map["Five of a kind"] = [cards]
        else:
            rank_map["Five of a kind"].append(cards)

    return rank_map, bid_map

def fill_maps_alt(rank_map: dict, bid_map: dict, input_line: str) -> tuple:
    card_split = input_line.split()
    cards = card_split[0]
    bid_map[cards] = int(card_split[1])
    symbol_map = {}
    for card in cards:
        symbol_map[card] = symbol_map.get(card, 0) + 1

    if len(symbol_map) == len(cards):  # all cards are distinct
        if "J" in symbol_map: 
            if "One pair" not in rank_map:
                rank_map["One pair"] = [cards]
            else:
                rank_map["One pair"].append(cards)
        else:
            if "High card" not in rank_map:
                rank_map["High card"] = [cards]
            else:
                rank_map["High card"].append(cards)
    elif len(symbol_map) == 4:  # one pair
        if "J" in symbol_map:
            if "Three of a kind" not in rank_map:
                rank_map["Three of a kind"] = [cards]
            else:
                rank_map["Three of a kind"].append(cards)
        else:
            if "One pair" not in rank_map:
                rank_map["One pair"] = [cards]
            else:
                rank_map["One pair"].append(cards)
    elif len(symbol_map) == 3:  # two pair or 3 of a kind
        for val in symbol_map.values():
            if val != 1:
                if val == 2:
                    if "J" in symbol_map:
                        if symbol_map["J"] == 1:
                            if "Full house" not in rank_map:
                                rank_map["Full house"] = [cards]
                            else:
                                rank_map["Full house"].append(cards)
                        else:
                            if "Four of a kind" not in rank_map:
                                rank_map["Four of a kind"] = [cards]
                            else:
                                rank_map["Four of a kind"].append(cards)
                    else:
                        if "Two pair" not in rank_map:
                            rank_map["Two pair"] = [cards]
                        else:
                            rank_map["Two pair"].append(cards)
                else:
                    if "J" in symbol_map:
                        if "Four of a kind" not in rank_map:
                            rank_map["Four of a kind"] = [cards]
                        else:
                            rank_map["Four of a kind"].append(cards)
                    else:
                        if "Three of a kind" not in rank_map:
                            rank_map["Three of a kind"] = [cards]
                        else:
                            rank_map["Three of a kind"].append(cards)
                break
    elif len(symbol_map) == 2:  # four of a kind or full house
        for val in symbol_map.values():
            if val == 4 or val == 1:  # four of a kind case
                if "J" in symbol_map:
                    if "Five of a kind" not in rank_map:
                        rank_map["Five of a kind"] = [cards]
                    else:
                        rank_map["Five of a kind"].append(cards)
                else:
                    if "Four of a kind" not in rank_map:
                        rank_map["Four of a kind"] = [cards]
                    else:
                        rank_map["Four of a kind"].append(cards)
            else:  # full house case
                if "J" in symbol_map:
                    if "Five of a kind" not in rank_map:
                        rank_map["Five of a kind"] = [cards]
                    else:
                        rank_map["Five of a kind"].append(cards)
                else:
                    if "Full house" not in rank_map:
                        rank_map["Full house"] = [cards]
                    else:
                        rank_map["Full house"].append(cards)
            break
    elif len(symbol_map) == 1:  # Five of a kind
        if "Five of a kind" not in rank_map:
            rank_map["Five of a kind"] = [cards]
        else:
            rank_map["Five of a kind"].append(cards)

    return rank_map, bid_map

def sort_function(card: str, alt=False):
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif not alt and card == "J":
        return 11
    elif alt and card == "J":
        return 1
    elif card == "T":
        return 10
    else:
        return int(card)


def get_winnings(rank_map: dict, bid_map: dict, alt=False) -> int:
    rank = 0
    winnings = 0
    card_types = [
        "High card",
        "One pair",
        "Two pair",
        "Three of a kind",
        "Full house",
        "Four of a kind",
        "Five of a kind",
    ]
    for card_type in card_types:
        if card_type in rank_map:
            sorted_cards = sorted(
                rank_map[card_type],
                key=lambda x: (
                    sort_function(x[0], alt),
                    sort_function(x[1], alt),
                    sort_function(x[2], alt),
                    sort_function(x[3], alt),
                    sort_function(x[4], alt),
                ),
            )
            for card in sorted_cards:
                rank += 1
                winnings += rank * bid_map[card]

    return winnings


if __name__ == "__main__":
    solution("test.txt")
    solution("day_7_puzzle_input.txt")
