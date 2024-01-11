def get_ranges_for_condition(
    condition: str, parts_dict: dict
) -> tuple:  # first : if rule accepted range, second: if rule not accepted range
    if "<" in condition:
        var, num_to_compare = condition.split("<")
        num_to_compare = int(num_to_compare)
        lo, hi = parts_dict[var]
        return (
            var,
            (lo, min(num_to_compare - 1, hi)),
            (max(num_to_compare, lo), hi),
        )
    else:
        var, num_to_compare = condition.split(">")
        num_to_compare = int(num_to_compare)
        lo, hi = parts_dict[var]
        return (var, (max(num_to_compare + 1, lo), hi), (lo, min(num_to_compare, hi)))


def get_product(parts_dict: dict):
    product = 1
    for lo, hi in parts_dict.values():
        product *= hi - lo + 1

    return product


def get_accepted_parts_advanced(workflows: dict):
    combinations = 0
    stack = [
        ("in", {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)})
    ]  # curr_workflow, x_range, m_range, a_range, s_range
    while stack:
        curr_workflow, parts_dict = stack.pop()
        if curr_workflow == "A":
            combinations += get_product(parts_dict)
        elif curr_workflow == "R":
            continue
        else:
            for rule_or_fallback in workflows[curr_workflow]:
                if ":" in rule_or_fallback:  # actual rule
                    condition, post = rule_or_fallback.split(":")
                    (
                        var,
                        combination_range_if_passed,
                        combination_range_if_failed,
                    ) = get_ranges_for_condition(condition, parts_dict)

                    if combination_range_if_passed[0] <= combination_range_if_passed[1]:
                        copy_dict = dict(parts_dict)
                        copy_dict[var] = combination_range_if_passed
                        stack.append((post, copy_dict))
                    if combination_range_if_failed[0] <= combination_range_if_failed[1]:
                        copy_dict = dict(parts_dict)
                        copy_dict[var] = combination_range_if_failed
                        parts_dict = copy_dict
                else:  # fallback
                    stack.append((rule_or_fallback, parts_dict))

    return combinations


def passes_condition(condition: str, parts: dict):
    if "<" in condition:
        var, num_to_compare = condition.split("<")
        return parts[var] < int(num_to_compare)
    if ">" in condition:
        var, num_to_compare = condition.split(">")
        return parts[var] > int(num_to_compare)


def get_accepted_parts(workflows: dict, parts: list[list]):
    total = 0
    for part_arr in parts:
        curr_workflow = "in"
        part_dict = {
            "x": int(part_arr[0].split("=")[1]),
            "m": int(part_arr[1].split("=")[1]),
            "a": int(part_arr[2].split("=")[1]),
            "s": int(part_arr[3].split("=")[1]),
        }

        rule_idx = 0
        while rule_idx != len(workflows[curr_workflow]):
            rule = workflows[curr_workflow][rule_idx]
            # print(f"curr part: {part_dict} curr workflow: {curr_worklow}")
            if ":" in rule:
                condition, post = rule.split(":")
                if passes_condition(condition, part_dict):
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
                        curr_workflow = post
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
                    curr_workflow = rule
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

    return get_accepted_parts(workflows, parts), get_accepted_parts_advanced(workflows)


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
