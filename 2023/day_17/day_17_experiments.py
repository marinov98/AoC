from queue import Queue, PriorityQueue
from math import sqrt


class BlockState:
    def __init__(
        self,
        direction: str,
        row: int,
        col: int,
        heat_counter: int,
        total_heat_loss: int,
        target_row: int,
        target_col: int,
    ):
        self.d = direction
        self.r = row
        self.c = col
        self.heat_counter = heat_counter
        self.total_heat_loss = total_heat_loss
        self.target_row = target_row
        self.target_col = target_col

    # Manhattan Distance
    def Manhattan(self) -> int:
        return abs(self.r - self.target_row) + abs(self.c - self.target_col)

    # Euclidean Distance
    def Euclidean(self):
        return sqrt((self.r - self.target_row) ** 2 + (self.c - self.target_col) ** 2)

    def heuristic(self):
        return self.total_heat_loss + self.Euclidean()

    def __eq__(self, other):
        return self.heuristic() == other.heuristic()

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def __gt__(self, other):
        return self.heuristic() >= other.heuristic()

    def get_properties(self) -> tuple:
        return self.total_heat_loss, self.r, self.c, self.d, self.heat_counter


def find_min_heat_loss_path_pq(
    block: list, heat_limit: int = 10, min_heat_limit: int = 4
) -> int:
    visited = set()
    rows = len(block)
    cols = len(block[0])
    pq = PriorityQueue()
    pq.put(BlockState("s", int(0), int(0), int(0), int(0), rows - 1, cols - 1))
    dirs = {"s": (0, 1), "d": (1, 0), "u": (-1, 0), "r": (0, -1)}
    while pq:
        curr_heat_loss, r, c, d, heat_counter = pq.get().get_properties()

        if r == rows - 1 and c == cols - 1 and heat_counter > min_heat_limit - 1:
            return curr_heat_loss

        if (d, r, c, heat_counter) in visited:
            continue

        visited.add((d, r, c, heat_counter))

        possible_moves = [d]
        if heat_counter > min_heat_limit - 1 and heat_counter < heat_limit:
            if d == "s":
                possible_moves = ["s", "u", "d"]
            elif d == "u":
                possible_moves = ["u", "s", "r"]
            elif d == "d":
                possible_moves = ["d", "s", "r"]
            elif d == "r":
                possible_moves = ["r", "u", "d"]
        elif heat_counter > heat_limit - 1:
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
                if (n_d, n_r, n_c, n_heat_counter) not in visited:
                    pq.put(
                        BlockState(
                            n_d,
                            n_r,
                            n_c,
                            n_heat_counter,
                            n_curr_heat_loss,
                            rows - 1,
                            cols - 1,
                        )
                    )

    return 0


def find_min_heat_loss_path_dfs(block: list, heat_limit: int = 3):
    visited = set()
    rows = len(block)
    cols = len(block[0])
    min_heat_loss = -1
    stack = [
        (  # direction, row, column, heat counter, current heat loss
            str("s"),
            int(0),
            int(0),
            int(0),
            int(0),
        )
    ]
    dirs = {"s": (0, 1), "d": (1, 0), "u": (-1, 0), "r": (0, -1)}
    while len(stack) != 0:
        d, r, c, heat_counter, curr_heat_loss = stack.pop()

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
                if n_r == rows - 1 and n_c == cols - 1:  # we found the exit
                    if min_heat_loss == -1:
                        min_heat_loss = n_curr_heat_loss
                    else:
                        min_heat_loss = min(min_heat_loss, n_curr_heat_loss)
                elif (n_d, n_r, n_c, n_heat_counter) not in visited:
                    stack.append((n_d, n_r, n_c, n_heat_counter, n_curr_heat_loss))

    return min_heat_loss


def find_min_heat_loss_path_bfs(block: list, heat_limit: int = 3):
    visited = set()
    rows = len(block)
    cols = len(block[0])
    min_heat_loss = -1
    queue = Queue()
    queue.put(
        (  # direction, row, column, heat counter, current heat loss
            str("s"),
            int(0),
            int(0),
            int(0),
            int(0),
        )
    )
    dirs = {"s": (0, 1), "d": (1, 0), "u": (-1, 0), "r": (0, -1)}
    while not queue.empty():
        d, r, c, heat_counter, curr_heat_loss = queue.get()

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
                if n_r == rows - 1 and n_c == cols - 1:  # we found the exit
                    if min_heat_loss == -1:
                        min_heat_loss = n_curr_heat_loss
                    else:
                        min_heat_loss = min(min_heat_loss, n_curr_heat_loss)
                elif (n_d, n_r, n_c, n_heat_counter) not in visited:
                    queue.put((n_d, n_r, n_c, n_heat_counter, n_curr_heat_loss))

    return min_heat_loss
