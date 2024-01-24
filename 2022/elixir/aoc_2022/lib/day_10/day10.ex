defmodule Day10 do
  @inputs ["lib/day_10/test2.txt", "lib/day_10/day10input.txt"]
  # @inputs ["lib/day_10/test.txt"]
  # @inputs ["lib/day_10/test2.txt"]
  @targets MapSet.new([20, 60, 100, 140, 180, 220])

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input =
      input_file
      |> File.read!()
      |> String.split("\n", trim: true)

    {part1(input), 0}
  end

  def part1(input) do
    input
    |> Enum.map(&String.split/1)
    |> simulation
    |> Enum.sum()
  end

  defp simulation(instructions, x \\ 1, cycle \\ 1, signal_strs \\ []) do
    case instructions do
      [] ->
        signal_strs

      _ ->
        [curr_instruction | rest] = instructions

        case length(curr_instruction) do
          1 ->
            case MapSet.member?(@targets, cycle + 1) do
              false ->
                simulation(rest, x, cycle + 1, signal_strs)

              true ->
                simulation(rest, x, cycle + 1, [x * (cycle + 1) | signal_strs])
            end

          2 ->
            val = curr_instruction |> List.last() |> String.to_integer()

            cond do
              MapSet.member?(@targets, cycle + 1) ->
                simulation(rest, x + val, cycle + 2, [x * (cycle + 1) | signal_strs])

              MapSet.member?(@targets, cycle + 2) ->
                simulation(rest, x + val, cycle + 2, [(x + val) * (cycle + 2) | signal_strs])

              true ->
                simulation(rest, x + val, cycle + 2, signal_strs)
            end
        end
    end
  end
end
