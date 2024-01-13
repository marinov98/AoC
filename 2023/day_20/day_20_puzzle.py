from queue import Queue


def is_original_state(flip_flops: dict, conjuctions: dict) -> bool:
    for ff_v in flip_flops.values():
        # make sure all flip flops are off
        if ff_v[1] == True:
            return False

    for c_v in conjuctions.values():
        # every memory has a remembered lo pulse state
        if c_v[1][0] != len(c_v[0].keys()):
            return False

    return True


def handle_broadcast_signals(broadcaster: list, flip_flops: dict, conjuctions: dict):
    total_pulse = {"l": 0, "h": 0}
    cycles = 0
    curr_level = Queue()
    next_level = Queue()
    for _ in range(1000):
        cycles += 1
        # low pulse from button module
        total_pulse["l"] += 1
        print(f"button -l-> broadcaster")

        for module in broadcaster:
            total_pulse["l"] += 1
            curr_level.put((module, "l", "broadcaster"))

        while curr_level.qsize() > 0:
            curr_module, pulse_type, parent_key = curr_level.get()
            print(
                 f"{parent_key} -{pulse_type}-> {curr_module}; "
            )
            ff_key = f"%{curr_module}"
            c_key = f"&{curr_module}"
            if ff_key in flip_flops:
                target_ff = flip_flops[ff_key]
                if pulse_type == "l":
                    # turn on, send high pulse
                    pulse_to_send = pulse_type
                    if not target_ff[1]:
                        pulse_to_send = "h"
                        target_ff[1] = True
                    else:
                        # turn off, send low pulse
                        pulse_to_send = "l"
                        target_ff[1] = False
                    for next_module in target_ff[0]:
                        total_pulse[pulse_to_send] += 1
                        # n_c_key = f"&{next_module}"
                        # if n_c_key in conjuctions:
                        #     curr_level.put((next_module, pulse_to_send, ff_key))
                        # else:
                        #     next_level.put((next_module, pulse_to_send, ff_key))
                        next_level.put((next_module, pulse_to_send, ff_key))
            if c_key in conjuctions:
                target_c = conjuctions[c_key]
                # print(f"{target_c}, {c_key}")
                if target_c[0][parent_key] != pulse_type:
                    target_c[0][parent_key] = pulse_type
                    if pulse_type == "l":
                        # add to low , subtract from high
                        target_c[1][0] += 1
                        target_c[1][1] -= 1
                    else:
                        # add to high , subtract from low
                        target_c[1][0] -= 1
                        target_c[1][1] += 1
                target_module_len = len(target_c[0])
                to_send = False
                pulse_to_send = pulse_type
                if target_c[1][0] == target_module_len:
                    pulse_to_send = "h"
                    to_send = True
                elif target_c[1][1] == target_module_len:
                    pulse_to_send = "l"
                    to_send = True
                # print(f"dict: {target_c[0]}, pulse: {pulse_to_send}")
                # all remembered inputs are the same
                if to_send:
                    for next_module in target_c[2]:
                        total_pulse[pulse_to_send] += 1
                        next_level.put((next_module, pulse_to_send, c_key))

            if curr_level.qsize() == 0:
                while next_level.qsize() > 0:
                    curr_level.put(next_level.get())

        if is_original_state(flip_flops, conjuctions):
            break
        print("\n")
    # print(f"cycles performed: {cycles}")
    # print(flip_flops)
    # print(conjuctions)
    # print(f"pulse bookkeeping: {total_pulse}")
    return (total_pulse["l"] * total_pulse["h"])


def handle_signals(broadcaster: list, flip_flops: dict, conjuctions: dict):
    return handle_broadcast_signals(broadcaster, flip_flops, conjuctions)


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
                flip_flops[curr_split[0]] = [curr_split[1].split(", "), False]
            elif line.startswith("&"):
                module_split = curr_split[1].split(", ")
                conjuctions[curr_split[0]] = [
                    {},  # inputs
                    [0, 0],
                    [module for module in module_split],
                ]

    for ff_key, ff_val in flip_flops.items():
        for input in ff_val[0]:
            c_key = f"&{input}"
            if c_key in conjuctions:
                conjuctions[c_key][0][ff_key] = "l"
                conjuctions[c_key][1][0] += 1
    for c_key, c_val in conjuctions.items():
        for output in c_val[2]:
            n_c_key = f"&{output}"
            if n_c_key in conjuctions:
                conjuctions[n_c_key][0][c_key] = "l"
                conjuctions[n_c_key][1][0] += 1


    # print(conjuctions["&db"])

    return handle_signals(broadcaster, flip_flops, conjuctions)


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        answers = solution_helper(input_file)
        print(answers)


if __name__ == "__main__":
    solution(
        [
            # "test.txt",
            "test2.txt",
            # "day_20_puzzle_input.txt"
        ]
    )
