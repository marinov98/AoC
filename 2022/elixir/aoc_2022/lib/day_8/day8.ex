defmodule Day8 do
  @inputs ["lib/day_8/test.txt", "lib/day_8/day8input.txt"]
  # @inputs ["lib/day_8/test.txt"]

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
    grid =
      input
      |> Enum.map(fn elem -> elem |> String.graphemes() |> Enum.map(&String.to_integer/1) end)

    rows = length(grid)
    cols = hd(grid) |> length

    for r <- 0..(rows - 1), c <- 0..(cols - 1), reduce: {0, MapSet.new()} do
      {num_visible, visible_set} ->
        {is_visible, visible_set} = visible?(grid, r, c, rows, cols, visible_set)

        case is_visible do
          true -> {num_visible + 1, visible_set}
          false -> {num_visible, visible_set}
        end
    end
    |> elem(0)
  end

  defp visible?(grid, r, c, rows, cols, visibles) do
    curr = get_in(grid, [Access.at(r), Access.at(c)])

    cond do
      r == 0 or c == 0 or r == rows - 1 or c == cols - 1 ->
        visibles = MapSet.put(visibles, {r, c, "e"})
        {true, visibles}

      is_visible_dir?(grid, r, c - 1, curr, visibles, "l") ->
        visibles = MapSet.put(visibles, {r, c, "l"})
        {true, visibles}

      is_visible_dir?(grid, r, c + 1, curr, visibles, "r") ->
        visibles = MapSet.put(visibles, {r, c, "r"})
        {true, visibles}

      is_visible_dir?(grid, r - 1, c, curr, visibles, "u") ->
        visibles = MapSet.put(visibles, {r, c, "u"})
        {true, visibles}

      is_visible_dir?(grid, r + 1, c, curr, visibles, "d") ->
        visibles = MapSet.put(visibles, {r, c, "d"})
        {true, visibles}

      true ->
        {false, visibles}
    end
  end

  defp is_visible_dir?(grid, r, c, val, visibles, dir) do
    curr = get_in(grid, [Access.at(r), Access.at(c)])

    cond do
      val > curr and
          (MapSet.member?(visibles, {r, c, dir}) or MapSet.member?(visibles, {r, c, "e"})) ->
        true

      curr == nil ->
        true

      val > curr ->
        case dir do
          "l" ->
            is_visible_dir?(grid, r, c - 1, val, visibles, dir)

          "r" ->
            is_visible_dir?(grid, r, c + 1, val, visibles, dir)

          "u" ->
            is_visible_dir?(grid, r - 1, c, val, visibles, dir)

          "d" ->
            is_visible_dir?(grid, r + 1, c, val, visibles, dir)
        end

      true ->
        false
    end
  end
end
