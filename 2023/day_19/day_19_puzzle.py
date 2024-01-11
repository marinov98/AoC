def passes_rule(rule: str, parts: dict):
    if "<" in rule:
        var, num_to_compare = rule.split("<")
        return parts[var] < int(num_to_compare)
    if ">" in rule:
        var, num_to_compare = rule.split(">")
        return parts[var] > int(num_to_compare)


def get_accepted_parts(workflows: dict, parts: list[list]):
    total = 0
    for part_arr in parts:
        curr_worklow = "in"
        part_dict = {
            "x": int(part_arr[0].split("=")[1]),
            "m": int(part_arr[1].split("=")[1]),
            "a": int(part_arr[2].split("=")[1]),
            "s": int(part_arr[3].split("=")[1]),
        }

        rule_idx = 0
        while rule_idx != len(workflows[curr_worklow]):
            rule = workflows[curr_worklow][rule_idx]
            # print(f"curr part: {part_dict} curr workflow: {curr_worklow}")
            if ":" in rule:
                rule, post = rule.split(":")
                if passes_rule(rule, part_dict):
                    if post in "AR":
                        if post == "A":
                            total += (
                                part_dict["x"]
                                + part_dict["m"]
                                + part_dict["a"]
                                + part_dict["s"]
                            )
                        break
                    else:
                        curr_worklow = post
                        rule_idx = 0
                else:
                    rule_idx += 1

            else:
                if rule in "AR":
                    if rule == "A":
                        total += (
                            part_dict["x"]
                            + part_dict["m"]
                            + part_dict["a"]
                            + part_dict["s"]
                        )
                    break
                else:
                    curr_worklow = rule
                    rule_idx = 0

    return total


def solution_helper(input_file: str) -> tuple:
    workflows = {}
    parts = []
    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            if line and line[0] != "{":
                target_split = line[:-1].split("{")
                workflows[target_split[0]] = target_split[1].split(",")
            elif line and line[0] == "{":
                parts.append(line[1:-1].split(","))

    return get_accepted_parts(workflows, parts), 0


def solution(inputs: list[str]):
    for input_file in inputs:
        answers = solution_helper(input_file)
        print(f"Answer P1 using '{input_file}' is: {answers[0]}")
        print(f"Answer P2 using '{input_file}' is: {answers[1]}")


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            "day_19_puzzle_input.txt"
        ]
    )
