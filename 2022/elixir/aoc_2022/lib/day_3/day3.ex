defmodule Day3 do
  @inputs ["lib/day_3/test.txt", "lib/day_3/day3input.txt"]
  @point_tracker %{
    "a" => 1,
    "b" => 2,
    "c" => 3,
    "d" => 4,
    "e" => 5,
    "f" => 6,
    "g" => 7,
    "h" => 8,
    "i" => 9,
    "j" => 10,
    "k" => 11,
    "l" => 12,
    "m" => 13,
    "n" => 14,
    "o" => 15,
    "p" => 16,
    "q" => 17,
    "r" => 18,
    "s" => 19,
    "t" => 20,
    "u" => 21,
    "v" => 22,
    "w" => 23,
    "x" => 24,
    "y" => 25,
    "z" => 26,
    "A" => 27,
    "B" => 28,
    "C" => 29,
    "D" => 30,
    "E" => 31,
    "F" => 32,
    "G" => 33,
    "H" => 34,
    "I" => 35,
    "J" => 36,
    "K" => 37,
    "L" => 38,
    "M" => 39,
    "N" => 40,
    "O" => 41,
    "P" => 42,
    "Q" => 43,
    "R" => 44,
    "S" => 45,
    "T" => 46,
    "U" => 47,
    "V" => 48,
    "W" => 49,
    "X" => 50,
    "Y" => 51,
    "Z" => 52
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

    {part1(input), part2(input)}
  end

  defp part1_utility(rucksack) do
    {left, right} = String.split_at(rucksack, div(String.length(rucksack), 2))

    char_set =
      left
      |> String.graphemes()
      |> Enum.reduce(MapSet.new(), &MapSet.put(&2, &1))

    right
    |> String.graphemes()
    |> Enum.reduce(MapSet.new(), fn elem, acc ->
      case MapSet.member?(char_set, elem) do
        true -> MapSet.put(acc, Map.get(@point_tracker, elem))
        false -> acc
      end
    end)
  end

  def part1(input) do
    input
    |> Enum.map(&part1_utility/1)
    |> Enum.flat_map(& &1)
    |> Enum.sum()
  end

  defp part2_utility(triplets) do
    [first | [second, third]] = triplets

    first_map =
      first
      |> String.graphemes()
      |> Enum.reduce(MapSet.new(), &MapSet.put(&2, &1))

    second_map =
      second
      |> String.graphemes()
      |> Enum.reduce(MapSet.new(), &MapSet.put(&2, &1))

    third
    |> String.graphemes()
    |> Enum.reduce(MapSet.new(), fn elem, acc ->
      case MapSet.member?(first_map, elem) and MapSet.member?(second_map, elem) do
        true -> MapSet.put(acc, Map.get(@point_tracker, elem))
        false -> acc
      end
    end)
  end

  def part2(input) do
    input
    |> Enum.chunk_every(3)
    |> Enum.map(&part2_utility/1)
    # just testing out flat map reduce (flat map |> sum seems more elegant)
    |> Enum.flat_map_reduce(0, &{[], &2 + List.first(MapSet.to_list(&1))})
    |> elem(1)

    # different variant
    # |> Enum.flat_map(& &1)
    # |> Enum.sum()
  end
end
