from queue import PriorityQueue


class ELEM:
    def __init__(self, steps, r, c):
        self.steps = steps
        self.r = r
        self.c = c

    def unpack(self):
        return self.steps, self.r, self.c

    def __lt__(self, other):
        return self.steps < other.steps

    def __eq__(self, other):
        return self.steps == other.steps

    def __gt__(self, other):
        return self.steps >= other.steps


def get_longest_path(grid: list[list], ro: int, co: int) -> int:
    pq = PriorityQueue()
    pq.put(ELEM(0, ro, co))
    rows = len(grid)
    cols = len(grid[0])
    visited = set([(ro, co)])
    while pq.qsize() > 0:
        steps, r, c = pq.get().unpack()

        if r == rows - 1 and grid[r][c] == ".":
            return abs(steps)

        possible_moves = []
        if grid[r][c] == ">":
            possible_moves = [(r, c + 1)]
        elif grid[r][c] == "<":
            possible_moves = [(r, c - 1)]
        elif grid[r][c] == "v":
            possible_moves = [(r + 1, c)]
        elif grid[r][c] == "^":
            possible_moves = [(r - 1, c)]
        else:
            possible_moves = [(r - 1, c), (r + 1, c), (r, c + 1), (r, c - 1)]

        for nr, nc in possible_moves:
            if -1 < nr < rows and -1 < nc < cols:
                if grid[nr][nc] != "#" and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    pq.put(
                        ELEM(steps - 1, nr, nc)
                    )  # we want negative steps to simulate a max priority queue and get the longest path

    return 0


def print_grid(grid: list[list]) -> None:
    for row in grid:
        print(*row, sep=" ")


def solution_helper(input_file: str):
    grid = []
    with open(input_file, "r") as file:
        for line in file:
            grid.append(list(line.strip()))

    # print_grid(grid)
    # find origin
    ro = 0
    co = 0
    for j in range(len(grid[0])):
        if grid[0][j] == ".":
            co = j

    return get_longest_path(grid, ro, co)


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        ans = solution_helper(input_file)
        print(f"Solution using file '{input_file}': {ans}")


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            # "day_23_puzzle_input.txt"
        ]
    )
