defmodule Day9 do
  @inputs ["lib/day_9/test.txt", "lib/day_9/day9input.txt"]
  # @inputs ["lib/day_9/test.txt"]
  # @inputs ["lib/day_9/test2.txt"]

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input =
      input_file
      |> File.read!()
      |> String.split("\n", trim: true)

    {part1(input), part2(input)}
  end

  def part1(input, h_r \\ 0, h_c \\ 0, t_r \\ 0, t_c \\ 0, tracker \\ MapSet.new()) do
    case Enum.empty?(input) do
      true ->
        tracker |> MapSet.size()

      false ->
        [curr | rest] = input
        curr_dir_split = String.split(curr, " ")
        curr_dir = curr_dir_split |> hd
        curr_moves = curr_dir_split |> List.last() |> String.to_integer()

        {h_r, h_c, t_r, t_c, tracker} =
          simulation_helper(curr_dir, curr_moves, h_r, h_c, t_r, t_c, tracker)

        part1(rest, h_r, h_c, t_r, t_c, tracker)
    end
  end

  defp simulation_helper(dir, moves, h_r, h_c, t_r, t_c, tracker) do
    tracker = MapSet.put(tracker, {t_r, t_c})

    case moves do
      0 ->
        {h_r, h_c, t_r, t_c, tracker}

      _ ->
        case dir do
          "R" ->
            h_c = h_c + 1
            {t_r, t_c} = fix_tail(h_r, h_c, t_r, t_c)
            simulation_helper(dir, moves - 1, h_r, h_c, t_r, t_c, tracker)

          "L" ->
            h_c = h_c - 1
            {t_r, t_c} = fix_tail(h_r, h_c, t_r, t_c)
            simulation_helper(dir, moves - 1, h_r, h_c, t_r, t_c, tracker)

          "D" ->
            h_r = h_r - 1
            {t_r, t_c} = fix_tail(h_r, h_c, t_r, t_c)
            simulation_helper(dir, moves - 1, h_r, h_c, t_r, t_c, tracker)

          "U" ->
            h_r = h_r + 1
            {t_r, t_c} = fix_tail(h_r, h_c, t_r, t_c)
            simulation_helper(dir, moves - 1, h_r, h_c, t_r, t_c, tracker)
        end
    end
  end

  defp fix_tail(h_r, h_c, t_r, t_c) do
    rd = h_r - t_r
    cd = h_c - t_c
    r_d = abs(rd)
    c_d = abs(cd)

    cond do
      # no need to change
      r_d < 2 and c_d < 2 ->
        {t_r, t_c}

      # h is above or below tail
      r_d > 1 and c_d == 0 ->
        cond do
          # tail below head
          rd < 0 ->
            {t_r - 1, t_c}

          # tail above head
          true ->
            {t_r + 1, t_c}
        end

      # h is to the left or right of tail
      c_d > 1 and r_d == 0 ->
        cond do
          # tail to the right of head
          cd < 0 ->
            {t_r, t_c - 1}

          # tail to the left of head
          true ->
            {t_r, t_c + 1}
        end

      # Diagonals
      r_d > 1 or c_d > 1 ->
        cond do
          # tail above head and to the left
          rd > 0 and cd > 0 ->
            {t_r + 1, t_c + 1}

          # tail below head and to the right
          rd < 0 and cd < 0 ->
            {t_r - 1, t_c - 1}

          # tail above head and to the right
          rd > 0 and cd < 0 ->
            {t_r + 1, t_c - 1}

          # tail below head and to the left
          rd < 0 and cd > 0 ->
            {t_r - 1, t_c + 1}
        end
    end
  end

  def part2(
        input,
        h_r \\ 0,
        h_c \\ 0,
        tail \\ [{0, 0}, {0, 0}, {0, 0}, {0, 0}, {0, 0}, {0, 0}, {0, 0}, {0, 0}, {0, 0}],
        tracker \\ MapSet.new()
      )

  def part2(
        input,
        _h_r,
        _h_c,
        _tail,
        tracker
      )
      when length(input) == 0,
      do: MapSet.size(tracker)

  def part2(
        input,
        h_r,
        h_c,
        tail,
        tracker
      ) do
    [curr | rest] = input
    curr_dir_split = String.split(curr, " ")
    curr_dir = curr_dir_split |> hd
    curr_moves = curr_dir_split |> List.last() |> String.to_integer()

    {h_r, h_c, tail, tracker} =
      simulation_helper2(curr_dir, curr_moves, h_r, h_c, tail, tracker)

    part2(rest, h_r, h_c, tail, tracker)
  end

  defp simulation_helper2(dir, moves, h_r, h_c, tail, tracker) do
    tracker = MapSet.put(tracker, List.last(tail))

    case moves do
      0 ->
        {h_r, h_c, tail, tracker}

      _ ->
        case dir do
          "R" ->
            h_c = h_c + 1
            tail = update_tail(h_r, h_c, tail)
            simulation_helper2(dir, moves - 1, h_r, h_c, tail, tracker)

          "L" ->
            h_c = h_c - 1
            tail = update_tail(h_r, h_c, tail)
            simulation_helper2(dir, moves - 1, h_r, h_c, tail, tracker)

          "D" ->
            h_r = h_r - 1
            tail = update_tail(h_r, h_c, tail)
            simulation_helper2(dir, moves - 1, h_r, h_c, tail, tracker)

          "U" ->
            h_r = h_r + 1
            tail = update_tail(h_r, h_c, tail)
            simulation_helper2(dir, moves - 1, h_r, h_c, tail, tracker)
        end
    end
  end

  defp update_tail(h_r, h_c, tail, new_tail \\ []) do
    case Enum.empty?(tail) do
      true ->
        Enum.reverse(new_tail)

      false ->
        [{t_r, t_c} | rest] = tail
        {t_r, t_c} = fix_tail(h_r, h_c, t_r, t_c)
        update_tail(t_r, t_c, rest, [{t_r, t_c} | new_tail])
    end
  end
end
