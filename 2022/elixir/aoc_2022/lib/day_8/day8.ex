defmodule Day8 do
  # @inputs ["lib/day_8/test.txt", "lib/day_8/day8input.txt"]
  @inputs ["lib/day_8/test.txt"]

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input =
      input_file
      |> File.read!()
      |> String.split("\n", trim: true)
      |> Enum.map(&String.graphemes/1)
    {part1(input), 0}
  end

  def part1(input) do
    0
  end
end
