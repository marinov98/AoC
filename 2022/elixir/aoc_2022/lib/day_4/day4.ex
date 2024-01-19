defmodule Day4 do
  @inputs ["lib/day_4/test.txt", "lib/day_4/day4input.txt"]

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
      |> Enum.map(fn curr_str ->
        curr_str
        |> String.trim()
        |> String.split(",")
      end)

    {part1(input), part2(input)}
  end

  def part1(input) do
    input
    |> Enum.reduce(0, &(part1_utility(&1) + &2))
  end

  defp part1_utility(ranges) do
    [s1 | rest] = List.first(ranges) |> String.split("-") |> Enum.map(&String.to_integer/1)
    [s2 | rest2] = List.last(ranges) |> String.split("-") |> Enum.map(&String.to_integer/1)
    e1 = List.first(rest)
    e2 = List.first(rest2)

    cond do
      s1 <= s2 and e1 >= e2 -> 1
      s2 <= s1 and e2 >= e1 -> 1
      true -> 0
    end
  end

  defp part2(input) do
    input
    |> Enum.reduce(0, &(part2_utility(&1) + &2))
  end

  defp part2_utility(ranges) do
    [s1 | rest] = List.first(ranges) |> String.split("-") |> Enum.map(&String.to_integer/1)
    [s2 | rest2] = List.last(ranges) |> String.split("-") |> Enum.map(&String.to_integer/1)
    e1 = List.first(rest)
    e2 = List.first(rest2)

    cond do
      s1 <= s2 and s2 <= e1 -> 1
      s2 <= s1 and s1 <= e2 -> 1
      true -> 0
    end
  end
end
