from queue import Queue


def handle_flip_flop_signals(
    flip_flop_key, flip_flops: dict, conjuctions: dict, pulse_type: str
):
    q = Queue()
    total_pulese = {"l": 1, "h": 0}

    q.put((flip_flop_key, pulse_type, flip_flop_key, str("ff")))
    while q.qsize() > 0:
        target_key, pulse_type, prev_key, module_type = q.get()
        if module_type == "ff":  # flip flop
            target_flip_flop = flip_flops[target_key]
            if pulse_type == "l":
                pulse_to_send = "h"
                if target_flip_flop[1] == "-":
                    # turn on, send high pulse
                    target_flip_flop[1] = "+"
                else:
                    # turn off, send low pulse
                    target_flip_flop[1] = "-"
                    pulse_to_send = "l"

                for module in flip_flops[flip_flop_key][0]:
                    flip_flop_key = f"%{module}"
                    conjuctions_key = f"&{module}"
                    if flip_flop_key in flip_flops:
                        q.put((flip_flop_key, pulse_to_send, flip_flop_key, "ff"))
                    elif conjuctions_key in conjuctions:
                        q.put((conjuctions_key, pulse_to_send, target_key, "in"))
        else:
            target_conjuction = conjuctions[target_key]
            if target_conjuction[0][prev_key] != pulse_type:
                target_conjuction[0][prev_key] = pulse_type
                if pulse_type == "l":
                    target_conjuction[1][0] += 1
                    target_conjuction[1][1] -= 1
                else:
                    target_conjuction[1][0] -= 1
                    target_conjuction[1][1] += 1
            curr_conjuction_modules = len(target_conjuction[0])
            to_send = False
            pulse_to_send = "h"
            if target_conjuction[1][0] == curr_conjuction_modules:
                to_send = True
            elif target_conjuction[1][1] == curr_conjuction_modules:
                to_send = True
                pulse_to_send = "l"
            if to_send:
                for module in target_conjuction[0].keys():
                    flip_flop_key = f"%{module}"
                    conjuctions_key = f"&{module}"
                    if flip_flop_key in flip_flops:
                        q.put((flip_flop_key, pulse_to_send, flip_flop_key, "ff"))
                    elif conjuctions_key in conjuctions:
                        q.put((conjuctions_key, pulse_to_send, target_key, "in"))


def handle_broadcast_signals(broadcaster: list, flip_flops: dict, conjuctions: dict):
    for module in broadcaster:
        flip_flop_key = f"%{module}"
        if flip_flop_key in flip_flops:
            handle_flip_flop_signals(flip_flop_key, flip_flops, conjuctions, "l")


def handle_signals(broadcaster: list, flip_flops: dict, conjuctions: dict):
    total_high_pulses = 0
    total_low_pulses = 1
    return total_high_pulses * total_low_pulses


def solution_helper(input_file: str):
    broadcaster = []
    flip_flops = {}
    conjuctions = {}
    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            curr_split = line.split(" -> ")
            if line.startswith("broadcaster"):
                broadcaster.extend(curr_split[1].split(", "))
            elif line.startswith("%"):
                flip_flops[curr_split[0]] = [curr_split[1].split(", "), "-"]
            elif line.startswith("&"):
                module_split = curr_split[1].split(", ")
                conjuctions[curr_split[0]] = [
                    {key: "l" for key in module_split},
                    [len(module_split), 0],
                ]

    return handle_signals(broadcaster, flip_flops, conjuctions)


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        answers = solution_helper(input_file)
        print(answers)


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            # "day_20_puzzle_input.txt"
        ]
    )
