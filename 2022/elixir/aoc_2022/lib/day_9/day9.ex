defmodule Day9 do
  @inputs ["lib/day_9/test.txt", "lib/day_9/day9input.txt"]
  # @inputs ["lib/day_9/test.txt"]

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
