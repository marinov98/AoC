defmodule Day1 do
  @inputs [ "lib/day_1/test.txt", "lib/day_1/day1input.txt" ]

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

    {{"Part 1 using '#{input_file}'", part1(input)}, {"Part 2 using '#{input_file}'", part2(input)}}
  end

  def part1(input) do
    input
    |> Enum.reduce(&max/2)
  end

  def part2(input) do
    input
    # alternative lazy method with sorting and taking the first 3
    #    |> Enum.sort(&(&1 >= &2))
    #    |> Enum.take(3)
    #    |> Enum.sum
    |> Enum.reduce({0, 0, 0}, fn cals, acc ->
                    cond do
                      cals > elem(acc, 0) -> {cals, elem(acc, 0), elem(acc, 1)}
                      cals > elem(acc, 1) -> {elem(acc, 0), cals, elem(acc, 1)}
                      cals > elem(acc, 2) -> {elem(acc, 0), elem(acc, 1), cals}
                      true -> acc
                    end
                  end)
    |> Tuple.sum()
  end
end
