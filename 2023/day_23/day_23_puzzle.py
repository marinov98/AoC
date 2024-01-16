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


# TODO: implement topological sorting first then run this
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


def dfs(pt: tuple, end: tuple, visited: set, graph: dict):
    if pt == end:
        return 0

    max_dist = -float("inf")
    visited.add(pt)
    for nx in graph[pt]:
        if nx not in visited:
            max_dist = max(max_dist, dfs(nx, end, visited, graph) + graph[pt][nx])
    visited.remove(pt)

    return max_dist


def get_longest_path_alt(grid: list[list], alt: bool = False):
    origin = (0, grid[0].index("."))
    end = (len(grid) - 1, grid[-1].index("."))

    points = [origin, end]
    rows = len(grid)
    cols = len(grid[0])

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "#":
                continue
            neighbors = 0
            possible_moves = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            for nr, nc in possible_moves:
                if -1 < nr < rows and -1 < nc < cols and grid[nr][nc] != "#":
                    neighbors += 1

            if neighbors > 2:
                points.append((r, c))
    graph = {pt: {} for pt in points}
    for sr, sc in points:
        stack = [(int(0), sr, sc)]
        visited = {(sr, sc)}

        while stack:
            steps, r, c = stack.pop()

            if steps != 0 and (r, c) in points:
                graph[(sr, sc)][(r, c)] = steps
                continue

            if not alt:
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
            else:
                possible_moves = [(r - 1, c), (r + 1, c), (r, c + 1), (r, c - 1)]

            for nr, nc in possible_moves:
                if (
                    -1 < nr < rows
                    and -1 < nc < cols
                    and grid[nr][nc] != "#"
                    and (nr, nc) not in visited
                ):
                    visited.add((nr, nc))
                    stack.append((steps + 1, nr, nc))
    return dfs(origin, end, set(), graph)


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
    # ro = 0
    # co = 0
    # for j in range(len(grid[0])):
    #     if grid[0][j] == ".":
    #         co = j

    return get_longest_path_alt(grid), get_longest_path_alt(grid, True)


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        ans = solution_helper(input_file)
        print(f"Solution(s) using file '{input_file}': {ans}")


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            "day_23_puzzle_input.txt"
        ]
    )
