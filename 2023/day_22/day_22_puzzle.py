from queue import Queue

if __name__ == "__main__":

    inputs = [
        # "test.txt"
        'day_22_puzzle_input.txt'
    ]

    bricks = []
    for input_file in inputs:
        with open(input_file, "r") as file:
            for line in file:
                brick_start, brick_end = line.strip().split("~")
                bricks.append(
                    [
                        *list(map(int, brick_start.split(","))),
                        *list(map(int, brick_end.split(","))),
                    ]
                )

    # sort by z value
    bricks.sort(key=lambda brick: brick[2])

    def is_overlapping(b1, b2):
        return max(b1[0], b2[0]) <= min(b1[3], b2[3]) and max(b1[1], b2[1]) <= min(
            b1[4], b2[4]
        )


    def find_solution(bricks: list):
        for i, brick in enumerate(bricks):
            bottom_z = 1
            for check in bricks[:i]:
                if is_overlapping(brick, check):
                    bottom_z = max(bottom_z, check[5] + 1)
            brick[5] += bottom_z - brick[2]
            brick[2] = bottom_z

        bricks.sort(key=lambda brick: brick[2])

        a_supports_b = {key: set() for key in range(len(bricks))}
        b_supports_a = {key: set() for key in range(len(bricks))}

        for j, upper in enumerate(bricks):
            for i, lower in enumerate(bricks[:j]):
                if is_overlapping(lower, upper) and upper[2] == lower[5] + 1:
                    a_supports_b[i].add(j)
                    b_supports_a[j].add(i)


        total = 0

    # part 1
    # for i in range(len(bricks)):
    #     if all(len(b_supports_a[j]) > 1 for j in a_supports_b[i]):
    #         total += 1

        # part 2
        for i in range(len(bricks)):
            q = Queue()
            falling = set()
            for j in a_supports_b[i]:
                if len(b_supports_a[j]) == 1:
                    falling.add(j)
                    q.put(j)

            falling.add(i)
            while q.qsize() > 0:
                j = q.get()
                for k in a_supports_b[j] - falling:
                    if b_supports_a[k] <= falling:
                        q.put(k)
                        falling.add(k)

            total += len(falling) - 1
        return total
    print(find_solution(bricks))

