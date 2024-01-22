defmodule Day10 do
  @inputs ["lib/day_10/test.txt", "lib/day_10/day10input.txt"]
  # @inputs ["lib/day_10/test.txt"]

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input =
      input_file
      |> File.read!()
  end
end
