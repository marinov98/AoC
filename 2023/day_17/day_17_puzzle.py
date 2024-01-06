from heapq import heappush, heappop


def find_min_heat_loss_path(block: list, heat_limit: int = 3):
    visited = set()
    rows = len(block)
    cols = len(block[0])
    min_heat_loss = 0
    pq = [
        (  # direction, row, column, heat counter, current heat loss
            int(0),
            int(0),
            int(0),
            str("s"),
            int(0),
        )
    ]
    dirs = {"s": (0, 1), "d": (1, 0), "u": (-1, 0), "r": (0, -1)}
    while pq:
        curr_heat_loss, r, c, d, heat_counter = heappop(pq)

        if r == rows - 1 and c == cols - 1:
            return curr_heat_loss

        if (d, r, c, heat_counter) in visited:
            continue

        visited.add((d, r, c, heat_counter))


        possible_moves = []
        if heat_counter < heat_limit:
            if d == "s":
                possible_moves = ["s", "u", "d"]
            elif d == "u":
                possible_moves = ["u", "s", "r"]
            elif d == "d":
                possible_moves = ["d", "s", "r"]
            elif d == "r":
                possible_moves = ["r", "u", "d"]
        else:
            # must rotate 90 degrees
            if d == "s":
                possible_moves = ["d", "u"]
            elif d == "u":
                possible_moves = ["s", "r"]
            elif d == "d":
                possible_moves = ["s", "r"]
            elif d == "r":
                possible_moves = ["d", "u"]

        for n_d in possible_moves:
            n_r, n_c = r + dirs[n_d][0], c + dirs[n_d][1]
            if -1 < n_r < rows and -1 < n_c < cols:
                n_heat_counter = (
                    heat_counter + 1 if n_d == d else 1
                )  # reset if changing direction
                n_curr_heat_loss = curr_heat_loss + block[n_r][n_c]
                heappush(pq, (n_curr_heat_loss, n_r, n_c, n_d, n_heat_counter))

    return min_heat_loss


def solution_helper(input_file: str) -> tuple:
    block = []
    with open(input_file, "r") as file:
        for line in file:
            block.append(list(map(int, list(line.strip()))))
    return find_min_heat_loss_path(block), 0


def print_grid(grid: list) -> None:
    for row in grid:
        print(*row, sep=" ")


def solution(files: list[str]) -> None:
    for input_file in files:
        answers = solution_helper(input_file)
        print(f"Solution P1 using '{input_file}': {answers[0]}")
        print(f"Solution P2 using '{input_file}': {answers[1]}")


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            "day_17_puzzle_input.txt"
        ]
    )
