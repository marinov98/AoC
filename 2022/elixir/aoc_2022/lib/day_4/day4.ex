defmodule Day4 do
  @inputs ["lib/day_4/test.txt", "lib/day_4/day4input.txt"]

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input = input_file |> File.read!() |> String.trim() |> String.split("\n")
    {part1(input), 0}
  end

  def part1(input) do
    input
    |> Enum.map(fn curr_str ->
      curr_str
      |> String.trim()
      |> String.split(",")
    end)
    # |> Enum.filter(&part1_filter(List.first(&1), List.last(&1)))
    |> Enum.reduce(0, &(part1_utility(&1) + &2))
  end

  defp part1_utility(ranges) do
    [s1 | e1] = List.first(ranges) |> String.split("-") |> Enum.map(&String.to_integer/1)
    [s2 | e2] = List.last(ranges) |> String.split("-") |> Enum.map(&String.to_integer/1)
    cond do
      s1 <= s2 and e1 >= e2 -> 1
      s2 <= s1 and e2 >= e1 -> 1
      true -> 0
    end
  end

  defp part1_filter(left, right) do
    s1 = String.to_integer(String.first(left))
    e1 = String.to_integer(String.last(left))

    s2 = String.to_integer(String.first(right))
    e2 = String.to_integer(String.last(right))

    cond do
      s1 <= s2 and e1 >= e2 -> true
      s2 <= s1 and e2 >= e1 -> true
      true -> false
    end
  end
end
