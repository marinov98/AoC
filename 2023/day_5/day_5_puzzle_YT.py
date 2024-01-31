inputs, *blocks = open("day_5_puzzle_input.txt").read().split("\n\n")

inputs = list(map(int, inputs.split(":")[1].split()))

seeds = []

for i in range(0, len(inputs), 2):
    seeds.append((inputs[i], inputs[i] + inputs[i + 1]))

for block in blocks:
    ranges = []
    for line in block.splitlines()[1:]:
        ranges.append(list(map(int, line.split())))
    new = []
    while len(seeds) > 0:
        start, end = seeds.pop()
        for dest_start, src_start, range_len in ranges:
            upper_bound = src_start + range_len
            os = max(start, src_start)
            oe = min(end, upper_bound)
            if os < oe:
                new.append((dest_start + os - src_start, dest_start + oe - src_start))
                if os > start:
                    seeds.append((start, os))
                if end > oe:
                    seeds.append((oe, end))
                break
        else:
            new.append((start, end))
    seeds = new

print(min(seeds)[0])
