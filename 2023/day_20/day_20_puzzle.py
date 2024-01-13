from queue import Queue


class FF:
    def __init__(self, id: str, outputs: list, state: bool = False):
        self.id = id
        self.outputs = outputs
        self.state = state

    def flip_and_send(self):
        pulse_to_send = None
        if not self.state:
            # turn on, send high pulse
            pulse_to_send = "h"
        else:
            # turn off, send low pulse
            pulse_to_send = "l"

        self.state = not self.state
        return pulse_to_send

    def __repr__(self):
        return f"{self.id}: outputs={self.outputs}, state={self.state}"


class CJ:
    def __init__(self, id: str, outputs: list):
        self.id = id
        self.inputs = {}
        self.outputs = outputs
        self.pulses = [0, 0]

    def update_inputs(self, key: str) -> None:
        if key not in self.inputs:
            # by default l is the remembered pulse
            self.inputs[key] = "l"
            self.pulses[0] += 1

    def update_and_send(self, pulse_type: str, key: str) -> str:
        if self.inputs[key] != pulse_type:
            self.inputs[key] = pulse_type
            if pulse_type == "l":
                self.pulses[0] += 1
                self.pulses[1] -= 1
            else:
                self.pulses[1] += 1
                self.pulses[0] -= 1

        if self.all_match(1):
            return "l"

        return "h"

    def all_match(self, idx) -> bool:
        if 0 < idx < 3:
            return self.pulses[idx] == len(self.inputs)
        return False

    def __repr__(self) -> str:
        return f"{self.id}: inputs={self.inputs}, outputs={self.outputs}, pulses={self.pulses}"


def is_original_state(flip_flops: dict[str, FF], conjuctions: dict[str, CJ]) -> bool:
    for ff_v in flip_flops.values():
        # make sure all flip flops are off
        if ff_v.state == True:
            return False

    for c_v in conjuctions.values():
        # every memory has a remembered lo pulse state
        if not c_v.all_match(0):
            return False

    return True


def handle_signals(
    broadcaster: list, flip_flops: dict[str, FF], conjuctions: dict[str, CJ]
) -> int:
    total_pulse = {"l": 0, "h": 0}
    cycles = 0
    q = Queue()
    for _ in range(1000):
        cycles += 1
        # low pulse from button module
        total_pulse["l"] += 1
        # print(f"button -l-> broadcaster")

        for module in broadcaster:
            total_pulse["l"] += 1
            q.put((module, "l", "broadcaster"))

        while q.qsize() > 0:
            curr_module, pulse_type, parent_key = q.get()
            # print(
            #      f"{parent_key} -{pulse_type}-> {curr_module}; "
            # )
            ff_key = f"%{curr_module}"
            c_key = f"&{curr_module}"
            if ff_key in flip_flops:
                target_ff = flip_flops[ff_key]
                if pulse_type == "l":
                    pulse_to_send = target_ff.flip_and_send()
                    for next_module in target_ff.outputs:
                        total_pulse[pulse_to_send] += 1
                        q.put((next_module, pulse_to_send, ff_key))
            elif c_key in conjuctions:
                target_c = conjuctions[c_key]
                pulse_to_send = target_c.update_and_send(pulse_type, parent_key)

                for next_module in target_c.outputs:
                    total_pulse[pulse_to_send] += 1
                    q.put((next_module, pulse_to_send, c_key))

    return total_pulse["l"] * total_pulse["h"]


def solution_helper(input_file: str) -> int:
    broadcaster = []
    flip_flops = {}
    conjuctions = {}
    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            id, outputs = line.split(" -> ")
            if line.startswith("broadcaster"):
                broadcaster.extend(outputs.split(", "))
            elif line.startswith("%"):
                flip_flops[id] = FF(id, outputs.split(", "), False)
            elif line.startswith("&"):
                module_split = outputs.split(", ")
                conjuctions[id] = CJ(id, module_split)

    for ff_key, ff_val in flip_flops.items():
        for input in ff_val.outputs:
            c_key = f"&{input}"
            if c_key in conjuctions:
                conjuctions[c_key].update_inputs(ff_key)

    for c_key, c_val in conjuctions.items():
        for output in c_val.outputs:
            n_c_key = f"&{output}"
            if n_c_key in conjuctions:
                conjuctions[n_c_key].update_inputs(c_key)

    return handle_signals(broadcaster, flip_flops, conjuctions)


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        answer = solution_helper(input_file)
        print(f"Solution P1 using '{input_file}': {answer}")


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            "test2.txt",
            "day_20_puzzle_input.txt",
        ]
    )
