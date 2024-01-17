import sympy

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

    def get_properties(self):
        return self.sx, self.sy, self.sz, self.vx, self.vy, self.vz

    def __repr__(self):
        return f"\nH initial sx: {self.sx} sy: {self.sy} sz: {self.sz} velocity: vx: {self.vx}  vy: {self.vy} vz: {self.vz} a: {self.a} b: {self.b} c: {self.c}"


def find_the_stone(hailstones: list[tuple]):

    xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")

    equations = []

    answers = []
    for i, (sx, sy, sz, vx, vy, vz) in enumerate(hailstones):
        equations.append((xr - sx) * (vy - vyr) - (yr - sy) * (vx - vxr))
        equations.append((yr - sy) * (vz - vzr) - (zr - sz) * (vy - vyr))
        if i < 2:
            continue
        answers = [soln for soln in sympy.solve(equations) if all(x % 1 == 0 for x in soln.values())]
        if len(answers) == 1:
            break
        
    answer = answers[0]
    return answer[xr] + answer[yr] + answer[zr]

def find_intersections(hailstones: list[HailStone], range_start: int, range_end: int) -> int:
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
    hailtstones_alt = None

    with open(input_file, "r") as file:
        hailtstones_alt = [tuple(map(int, line.replace("@", ",").split(","))) for line in file]
        for line in file:
            line = line.strip()
            hailstones.append(HailStone(*map(int, line.replace("@", ",").split(","))))

    return find_intersections(hailstones, 200000000000000, 400000000000000), find_the_stone(hailtstones_alt)


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
