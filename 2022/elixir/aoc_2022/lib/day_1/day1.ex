defmodule Day1 do
  @inputs ["lib/day_1/test.txt", "lib/day_1/day1input.txt"]

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input =
      input_file
      |> File.read!()
      |> String.split("\n\n")

    {{"Part 1 using '#{input_file}'", part1(input)},
     {"Part 2 using '#{input_file}'", part2(input)}}
  end

  def part1(input) do
    input
    |> Enum.reduce(0, &(&1 |> transform_to_sum() |> max(&2)))
  end

  def part2(input) do
    input
    |> Enum.reduce({0, 0, 0}, fn elem, acc ->
      cals = elem |> transform_to_sum()

      cond do
        cals > elem(acc, 0) -> {cals, elem(acc, 0), elem(acc, 1)}
        cals > elem(acc, 1) -> {elem(acc, 0), cals, elem(acc, 1)}
        cals > elem(acc, 2) -> {elem(acc, 0), elem(acc, 1), cals}
        true -> acc
      end
    end)
    |> Tuple.sum()

    # alternative lazy method with sorting and taking the first 3
    # input
    # |> Enum.map(&transform_to_sum/1)
    # |> Enum.sort(&(&1 >= &2))
    # |> Enum.take(3)
    # |> Enum.sum()
  end

  defp transform_to_sum(string) do
    string
    |> String.split("\n", trim: true)
    |> Enum.map(&String.to_integer/1)
    |> Enum.sum()
  end
end
