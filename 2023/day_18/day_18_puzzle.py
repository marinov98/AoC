def print_grid(grid: list) -> None:
    for row in grid:
        print(*row, sep=" ")

def get_dir_and_steps(line: str, alt = False):
    if not alt:
        input = line.split(" ")
        return input[0], int(input[1]), input[2]
    else:
        _, _, hex = line.split()
        hex = hex[2: -1]
        return _, int(0), hex



def solution_helper(input_file: str, alt = False) -> int:
    dirs = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    outside = 0
    points = [(0, 0)]
    with open(input_file, "r") as file:
        for line in file:
            d, steps, hex = get_dir_and_steps(line.strip(), alt)
            dr, dc = 0, 0
            if not alt:
                dr, dc = dirs[d]
            else:
                dr, dc = dirs["RDLU"[int(hex[-1])]]
                steps = int(hex[:-1], 16)
            outside += steps
            r, c = points[-1]
            points.append((r + dr * steps, c + dc * steps))

    area = (
        abs(
            sum(
                points[i][0] * (points[i - 1][1] - points[(i + 1) % len(points)][1])
                for i in range(len(points))
            )
        )
        // 2
    )
    inner = area - outside // 2 + 1

    return outside + inner


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        answer = solution_helper(input_file)
        print(f"Answer P1 using '{input_file}': {answer}")
        answer = solution_helper(input_file, True)
        print(f"Answer P2 using '{input_file}': {answer}")


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            "day_18_puzzle_input.txt"
        ]
    )
