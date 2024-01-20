defmodule Day6 do
  @inputs ["lib/day_6/test.txt", "lib/day_6/day6input.txt"]
  # @inputs ["lib/day_6/test.txt"]

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input =
      input_file
      |> File.read!()
      |> String.trim()
      |> String.split("\n")

    {part1(input), part2(input)}
  end

  def part1(input) do
    input
    |> Enum.map(&part1_helper/1)
  end

  def part1_helper(input, left \\ 0, right \\ 0, tracker \\ []) do
    cond do
      length(tracker) == 4 and length(Enum.uniq(tracker)) == 4 ->
        right

      true ->
        case right - left > 3 do
          true ->
            [_ | tracker] = tracker
            tracker = List.insert_at(tracker, -1, String.at(input, right))
            part1_helper(input, left + 1, right + 1, tracker)

          false ->
            tracker = List.insert_at(tracker, -1, String.at(input, right))
            part1_helper(input, left, right + 1, tracker)
        end
    end
  end

  def part2(input) do
    input
    |> Enum.map(&part2_helper/1)
  end

  def part2_helper(input, left \\ 0, right \\ 0, tracker \\ []) do
    cond do
      length(tracker) == 14 and length(Enum.uniq(tracker)) == 14 ->
        right

      true ->
        case right - left > 13 do
          true ->
            [_ | tracker] = tracker
            tracker = List.insert_at(tracker, -1, String.at(input, right))
            part2_helper(input, left + 1, right + 1, tracker)

          false ->
            tracker = List.insert_at(tracker, -1, String.at(input, right))
            part2_helper(input, left, right + 1, tracker)
        end
    end
  end
end
