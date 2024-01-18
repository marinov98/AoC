defmodule Day2 do
  @inputs ["lib/day_2/test.txt", "lib/day_2/day2input.txt"]
  @shape_points %{
    # Rock
    "X" => 1,
    # Paper
    "Y" => 2,
    # Scissor
    "Z" => 3
  }

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
      |> Enum.map(&String.split/1)

    {part1(input), part2(input)}
  end

  defp handle_match(opp, pl) do
    guarantee =
      Map.get(@shape_points, pl)

    cond do
      # Rock case
      pl == "X" and opp == "A" -> 3 + guarantee
      pl == "X" and opp == "B" -> 0 + guarantee
      pl == "X" and opp == "C" -> 6 + guarantee
      # Paper Case
      pl == "Y" and opp == "A" -> 6 + guarantee
      pl == "Y" and opp == "B" -> 3 + guarantee
      pl == "Y" and opp == "C" -> 0 + guarantee
      # Scissor Case
      pl == "Z" and opp == "A" -> 0 + guarantee
      pl == "Z" and opp == "B" -> 6 + guarantee
      pl == "Z" and opp == "C" -> 3 + guarantee
      true -> 0
    end
  end

  defp handle_match2(opp, pl) do
    cond do
      # Lose
      pl == "X" and opp == "A" -> 0 + Map.get(@shape_points, "Z")
      pl == "X" and opp == "B" -> 0 + Map.get(@shape_points, "X")
      pl == "X" and opp == "C" -> 0 + Map.get(@shape_points, "Y")
      # Draw
      pl == "Y" and opp == "A" -> 3 + Map.get(@shape_points, "X")
      pl == "Y" and opp == "B" -> 3 + Map.get(@shape_points, "Y")
      pl == "Y" and opp == "C" -> 3 + Map.get(@shape_points, "Z")
      # Win
      pl == "Z" and opp == "A" -> 6 + Map.get(@shape_points, "Y")
      pl == "Z" and opp == "B" -> 6 + Map.get(@shape_points, "Z")
      pl == "Z" and opp == "C" -> 6 + Map.get(@shape_points, "X")
      true -> 0
    end
  end

  def part1(input) do
    input
    |> Enum.reduce(0, fn elems, acc ->
      handle_match(List.first(elems), List.last(elems)) + acc
    end)
  end

  def part2(input) do
    input
    |> Enum.reduce(0, fn elems, acc ->
      handle_match2(List.first(elems), List.last(elems)) + acc
    end)
  end
end
