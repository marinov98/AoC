def solution(input_file: str) -> None:
    solution_helper(input_file)


def solution_helper(input_file: str) -> None:
    galaxy = []
    with open(input_file) as file:
        for line in file:
            galaxy.append(line.strip())
    expansion_tracker, old_galaxy_locations = expand_galaxy(galaxy)
    record_shortest_paths(old_galaxy_locations, expansion_tracker)


def expand_galaxy(initial_galaxy: list) -> tuple:
    rows = len(initial_galaxy)
    cols = len(initial_galaxy[0])
    expansion_tracker = set()
    for i in range(rows):
        if has_no_galaxy("row", i, initial_galaxy):
            expansion_tracker.add(("r", i))

    for j in range(cols):
        if has_no_galaxy("col", j, initial_galaxy):
            expansion_tracker.add(("c", j))

    galaxy_locations = []
    for k in range(rows):
        for l in range(cols):
            if initial_galaxy[k][l] != ".":
                galaxy_locations.append((k, l))

    return expansion_tracker, galaxy_locations


def has_no_galaxy(check_type: str, check_num, initial_galaxy: list) -> bool:
    if check_type == "row":
        for col in initial_galaxy[check_num]:
            if col == "#":
                return False
        return True
    elif check_type == "col":
        for row_str in initial_galaxy:
            if row_str[check_num] == "#":
                return False
        return True
    return False


def record_shortest_paths(galaxy_locations: list, expansion_tracker: set) -> None:
    total = 0
    total_1 = 0
    total_2 = 0
    second_total = 0
    num_nodes = len(galaxy_locations)
    # print(galaxy_locations)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            total += get_dist(
                galaxy_locations[i], galaxy_locations[j], expansion_tracker, 2
            )
            total_1 += get_dist(
                galaxy_locations[i], galaxy_locations[j], expansion_tracker, 10
            )
            total_2 += get_dist(
                galaxy_locations[i], galaxy_locations[j], expansion_tracker, 100
            )
            second_total += get_dist(
                galaxy_locations[i], galaxy_locations[j], expansion_tracker
            )

    print(f"Part 1 Sum of shortest paths with offset {2}: {total}")
    print(f"Part 1 Sum of shortest paths with offset {10}: {total_1}")
    print(f"Part 1 Sum of shortest paths with offset {100}: {total_2}")
    print(f"Part 2 Sum of shortest paths with offset {1000000}: {second_total}")


def get_dist(
    galaxy: tuple,
    galaxy_to_compare: tuple,
    expansion_tracker: set,
    expansion_offset: int = 1000000,
) -> int:
    r1, c1 = galaxy
    r2, c2 = galaxy_to_compare

    ans = 0
    r1, r2 = min(r1, r2), max(r1, r2)
    c1, c2 = min(c1, c2), max(c1, c2)
    for i in range(r1, r2):
        ans += 1
        if ("r", i) in expansion_tracker:
            ans += expansion_offset - 1
    for j in range(c1, c2):
        ans += 1
        if ("c", j) in expansion_tracker:
            ans += expansion_offset - 1
    return ans


if __name__ == "__main__":
    # solution("test.txt")
    solution("day_11_puzzle_input.txt")
