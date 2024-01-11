workflow_formats, _ = open("day_19_puzzle_input.txt").read().split("\n\n")

workflows = {}

for line in workflow_formats.splitlines():
    name, rest = line[:-1].split("{")
    rules = rest.split(",")
    workflows[name] = ([], rules.pop())
    for rule in rules:
        condition, post = rule.split(":")
        key = condition[0]
        cmp = condition[1]
        n = int(condition[2:])
        workflows[name][0].append((key, cmp, n, post))

def count(parts_dict, name = "in"):
    if name == "R":
        return 0
    if name == "A":
        product = 1
        for lo, hi in parts_dict.values():
            product *= hi - lo + 1
        return product
    
    rules, fallback = workflows[name]

    total = 0

    for key, cmp, n, target in rules:
        lo, hi = parts_dict[key]
        if cmp == "<":
            T = (lo, min(n - 1, hi))
            F = (max(n, lo), hi)
        else:
            T = (max(n + 1, lo), hi)
            F = (lo, min(n, hi))
        if T[0] <= T[1]:
            copy_dict = dict(parts_dict)
            copy_dict[key] = T
            total += count(copy_dict, target)
        if F[0] <= F[1]:
            parts_dict = dict(parts_dict)
            parts_dict[key] = F
        else:
            break
    else:
        total += count(parts_dict, fallback)
            
    return total

print(count({key: (1, 4000) for key in "xmas"}))
