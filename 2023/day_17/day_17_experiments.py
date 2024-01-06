from queue import Queue

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
