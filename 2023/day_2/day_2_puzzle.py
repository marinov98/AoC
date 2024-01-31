def solution(input_file: str, input_red: int, input_blue: int, input_green: int) -> None:
    first_answer = 0
    second_answer = 0
    with open(input_file, "r") as file:
        while True:
            next_line = file.readline()

            if not next_line:
                break

            game_id, game_max_red, game_max_green, game_max_blue = get_input_data(next_line.strip())
            # part 1
            if (game_max_red <= input_red and game_max_blue <= input_blue and game_max_green <= input_green):
                first_answer += game_id
            # part 2
            second_answer += game_max_blue * game_max_green * game_max_red




    print("Answer to the first puzzle should be:", first_answer)
    print("Answer to the second puzzle should be:", second_answer)

def get_input_data(input_line: str) -> tuple:
    game_split = input_line.split(": ")
    game_id = int(game_split[0].split(" ")[1])
    print("\nGame ID is:", game_id)
    games = game_split[1].split("; ")
    print("Games are:\n", games)
    max_red = 0
    max_blue = 0
    max_green = 0
    for game in games:
        cubes = game.split(", ")
        for cube in cubes:
            cube_metadata = cube.split(" ")
            if cube_metadata[1] == "red":
                max_red = max(max_red, int(cube_metadata[0]))
            elif cube_metadata[1] == "green":
                max_green = max(max_green, int(cube_metadata[0]))
            elif cube_metadata[1] == "blue":
                max_blue = max(max_blue, int(cube_metadata[0]))

    print(f"Current Maxes: {max_red} red, {max_blue} blue, {max_green} green")
    return (game_id, max_red, max_green, max_blue)


if __name__ == "__main__":
    solution("day_2_puzzle_input.txt", 12, 14, 13)
