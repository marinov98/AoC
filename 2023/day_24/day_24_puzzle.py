class HailStone:
    def __init__(self, sx, sy, sz, vx, vy, vz):
        self.sx = sx
        self.sy = sy
        self.sz = sz

        self.vx = vx
        self.vy = vy
        self.vz = vz

        self.a = vy
        self.b = -vx
        self.c = vy * sx - vx * sy

    def __repr__(self):
        return f"\nH initial sx: {self.sx} sy: {self.sy} sz: {self.sz} velocity: vx: {self.vx}  vy: {self.vy} vz: {self.vz} a: {self.a} b: {self.b} c: {self.c}"


def find_intersections(hailstones: list[HailStone], range_start, range_end):
    total = 0
    for i, hs1 in enumerate(hailstones):
        for hs2 in hailstones[:i]:
            if hs1.a * hs2.b == hs1.b * hs2.a:  # parallel
                continue

            intercept_x = (hs1.c * hs2.b - hs2.c * hs1.b) / (
                hs1.a * hs2.b - hs2.a * hs1.b
            )
            intercept_y = (hs2.c * hs1.a - hs1.c * hs2.a) / (
                hs1.a * hs2.b - hs2.a * hs1.b
            )

            if (
                range_start <= intercept_x <= range_end
                and range_start <= intercept_y <= range_end
            ):
                if all(
                    (intercept_x - hs.sx) * hs.vx >= 0
                    and (intercept_y - hs.sy) * hs.vy >= 0
                    for hs in (hs1, hs2)
                ):
                    total += 1

    return total


def solution_helper(input_file: str):
    hailstones = []
    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            hailstones.append(HailStone(*map(int, line.replace("@", ",").split(","))))

    return find_intersections(hailstones, 200000000000000, 400000000000000)
    # return find_intersections(hailstones, 7, 27)


def solution(inputs: list[str]) -> None:
    for input_file in inputs:
        print(f"Solution(s) given '{input_file}':", solution_helper(input_file))


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            "day_24_puzzle_input.txt"
        ]
    )
