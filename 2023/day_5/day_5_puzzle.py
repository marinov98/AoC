def solution(input_file: str) -> None:
    seeds = []
    unmapped_seeds = []
    seeds_alt = []
    unmapped_seeds_alt = []
    with open(input_file, "r") as file:
        for line in file:
            if line[0].isdigit() or line.startswith("seeds"):
                seeds, unmapped_seeds = process_maps(
                    line.strip(), seeds, unmapped_seeds
                )
                seeds_alt, unmapped_seeds_alt = process_maps_alt(
                    line.strip(), seeds_alt, unmapped_seeds_alt
                )
            elif "map:" in line:
                if len(seeds) != 0:
                    unmapped_seeds.extend(seeds)
                seeds = []
                if len(seeds_alt) != 0:
                    unmapped_seeds_alt.extend(seeds_alt)
                seeds_alt = []
    seeds.extend(unmapped_seeds)
    seeds_alt.extend(unmapped_seeds_alt)
    print(
        f"Answer to the first puzzle using file '{input_file}' should be:", min(seeds)
    )
    print(
        f"Answer to the second puzzle using file '{input_file}' should be:",
        min(seeds_alt)[0],
    )


def process_maps(input_line: str, mapped_seeds: list, unmapped_seeds: list) -> tuple:
    if input_line.startswith("seeds:"):
        # get the seeds
        seed_split = input_line.split(": ")
        return [], list(map(int, seed_split[1].split(" ")))
    else:  # getting numbers
        map_split = input_line.split(" ")
        curr_range = list(map(int, map_split))
        dest_start = curr_range[0]
        src_start = curr_range[1]
        range_len = curr_range[2]
        unmapped_new_seeds = []
        for seed in unmapped_seeds:
            if src_start <= seed < (src_start + range_len):
                mapped_seeds.append(dest_start + seed - src_start)
            else:
                unmapped_new_seeds.append(seed)
        return mapped_seeds, unmapped_new_seeds


def process_maps_alt(
    input_line: str, mapped_seeds: list, unmapped_seeds: list
) -> tuple:
    if input_line.startswith("seeds:"):
        # get the seeds (for Part 2 create the ranges)
        seed_split = input_line.split(": ")
        seed_config = list(map(int, seed_split[1].split(" ")))
        curr_start_range = 0
        curr_range_len = 0
        initial_ranges = []
        for i, config in enumerate(seed_config):
            if i % 2 == 0:
                curr_start_range = config
            else:
                curr_range_len = config
                initial_ranges.append(
                    (curr_start_range, curr_start_range + curr_range_len)
                )
        return [], initial_ranges
    # calculate mappings
    map_split = input_line.split(" ")
    curr_range = list(map(int, map_split))
    dest_start = curr_range[0]
    src_start = curr_range[1]
    range_len = curr_range[2]
    unmapped_new_ranges = []
    for start, end in unmapped_seeds:
        upper_bound = src_start + range_len
        if start >= src_start and end <= upper_bound:  # case 1
            mapped_range_start = dest_start + start - src_start
            mapped_range_end = dest_start + end - src_start
            mapped_seeds.append((mapped_range_start, mapped_range_end))
        elif start > upper_bound or end < src_start:  # case 2
            unmapped_new_ranges.append((start, end))
        elif start >= src_start and end > upper_bound:  # case 3
            mapped_range_start = dest_start + start - src_start
            mapped_range_end = dest_start + upper_bound - src_start
            mapped_seeds.append((mapped_range_start, mapped_range_end))
            unmapped_new_ranges.append((upper_bound, end))
        elif src_start > start and end <= upper_bound:  # case 4
            mapped_range_start = dest_start
            mapped_range_end = dest_start + end - src_start
            mapped_seeds.append((mapped_range_start, mapped_range_end))
            unmapped_new_ranges.append((start, src_start))
        elif start < src_start and end > upper_bound:  # case 5
            mapped_range_start = dest_start + src_start - src_start
            mapped_range_end = dest_start + upper_bound - src_start
            mapped_seeds.append((mapped_range_start, mapped_range_end))
            unmapped_new_ranges.append((start, src_start))
            unmapped_new_ranges.append((upper_bound, end))
    return mapped_seeds, unmapped_new_ranges


if __name__ == "__main__":
    solution("test.txt")
    solution("day_5_puzzle_input.txt")
