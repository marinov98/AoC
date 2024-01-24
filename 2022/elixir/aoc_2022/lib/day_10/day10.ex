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
      |> Enum.map(&String.split/1)

    # part2(input)}
    {part1(input), :not_implemented}
  end

  @doc """
    Part 1 of the puzzle
  """
  def part1(input) do
    input
    |> simulation

    # alternative method
    # |> simulation_alt
    # |> Enum.drop(20)
    # |> Enum.take_every(40)
    # |> Enum.reduce(0, fn {elem, cycle}, sum ->
    #   sum + elem * cycle
    # end)
  end

  @spec simulation(list(String.t()), integer(), integer(), integer()) :: integer()
  defp simulation(instructions, x \\ 1, cycle \\ 1, signal_strs_sum \\ 0) do
    case instructions do
      [] ->
        signal_strs_sum

      _ ->
        [curr_instruction | rest] = instructions

        case length(curr_instruction) do
          1 ->
            case MapSet.member?(@targets, cycle + 1) do
              false ->
                simulation(rest, x, cycle + 1, signal_strs_sum)

              true ->
                simulation(rest, x, cycle + 1, x * (cycle + 1) + signal_strs_sum)
            end

          2 ->
            val = curr_instruction |> List.last() |> String.to_integer()

            cond do
              MapSet.member?(@targets, cycle + 1) ->
                simulation(rest, x + val, cycle + 2, x * (cycle + 1) + signal_strs_sum)

              MapSet.member?(@targets, cycle + 2) ->
                simulation(rest, x + val, cycle + 2, (x + val) * (cycle + 2) + signal_strs_sum)

              true ->
                simulation(rest, x + val, cycle + 2, signal_strs_sum)
            end
        end
    end
  end

  @doc """
    Part 2 of the puzzle
  """
  def part2(input) do
    input
    |> simulation_alt
  end

  @spec simulation_alt(list(String.t()), integer(), list(tuple())) :: list(tuple())
  defp simulation_alt(instructions, x \\ 1, history \\ [{1, 0}]) do
    case Enum.empty?(instructions) do
      true ->
        cycle = history |> hd |> elem(1)
        Enum.reverse([{x, cycle + 1} | history])

      false ->
        [curr_instruction | rest] = instructions

        case length(curr_instruction) do
          1 ->
            cycle = history |> hd |> elem(1)
            simulation_alt(rest, x, [{x, cycle + 1} | history])

          2 ->
            val = curr_instruction |> List.last() |> String.to_integer()
            cycle = history |> hd |> elem(1)

            history = [{x, cycle + 1} | history]
            history = [{x, cycle + 2} | history]
            simulation_alt(rest, x + val, history)
        end
    end
  end
end
