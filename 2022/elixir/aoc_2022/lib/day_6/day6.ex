defmodule Day6 do
  @inputs ["lib/day_6/test.txt", "lib/day_6/day6input.txt"]

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input =
      input_file
      |> File.read!()
      |> String.trim()
    # {part1(input), part2(input)}
  end
  
end
