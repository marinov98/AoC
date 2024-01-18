defmodule Day1 do
  @inputs ["lib/day_1/test.txt", "lib/day_1/day_1_input.txt"]

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input = input_file
    |> File.read!()
    |> String.split("\n\n")
    |> Enum.map(fn curr_str ->
      curr_str
      |> String.trim()
      |> String.split("\n")
      |> Enum.map(&String.to_integer/1)
      |> Enum.sum()
    end)

    {part1(input), part2(input)}
  end

  def part1(input) do
    input
    |> Enum.reduce(&max/2)
  end

  def part2(input) do
    input
    |> Enum.sort(&(&1 >= &2))
    |> Enum.take(3)
    |> Enum.sum
  end
end
