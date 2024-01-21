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
      |> Enum.map(fn elem -> elem |> String.graphemes() |> Enum.map(&String.to_integer/1) end)

    {part1(input), part2(input)}
  end

  def part1(grid) do
    rows = length(grid)
    cols = hd(grid) |> length

    dp =
      for row_edge <- 0..(rows - 1), reduce: MapSet.new() do
        acc ->
          acc = MapSet.put(acc, {row_edge, 0, "e"})
          MapSet.put(acc, {row_edge, cols - 1, "e"})
      end

    dp =
      for col_edge <- 1..(cols - 2), reduce: dp do
        acc ->
          acc = MapSet.put(acc, {0, col_edge, "e"})
          MapSet.put(acc, {rows - 1, col_edge, "e"})
      end

    for r <- 1..(rows - 2), c <- 1..(cols - 2), reduce: {MapSet.size(dp), dp} do
      {num_visible, dp} ->
        {is_visible, dp} = visible?(grid, r, c, rows, cols, dp)

        case is_visible do
          true -> {num_visible + 1, dp}
          false -> {num_visible, dp}
        end
    end
    |> elem(0)
  end

  defp visible?(grid, r, c, rows, cols, dp) do
    curr = get_in(grid, [Access.at(r), Access.at(c)])

    cond do
      r == 0 or c == 0 or r == rows - 1 or c == cols - 1 ->
        dp = MapSet.put(dp, {r, c, "e"})
        {true, dp}

      is_visible_dir?(grid, r, c - 1, curr, dp, "l") ->
        dp = MapSet.put(dp, {r, c, "l"})
        {true, dp}

      is_visible_dir?(grid, r, c + 1, curr, dp, "r") ->
        dp = MapSet.put(dp, {r, c, "r"})
        {true, dp}

      is_visible_dir?(grid, r - 1, c, curr, dp, "u") ->
        dp = MapSet.put(dp, {r, c, "u"})
        {true, dp}

      is_visible_dir?(grid, r + 1, c, curr, dp, "d") ->
        dp = MapSet.put(dp, {r, c, "d"})
        {true, dp}

      true ->
        {false, dp}
    end
  end

  defp is_visible_dir?(grid, r, c, val, dp, dir) do
    curr = get_in(grid, [Access.at(r), Access.at(c)])

    cond do
      val > curr and
          (MapSet.member?(dp, {r, c, dir}) or MapSet.member?(dp, {r, c, "e"})) ->
        true

      val > curr ->
        case dir do
          "l" ->
            is_visible_dir?(grid, r, c - 1, val, dp, dir)

          "r" ->
            is_visible_dir?(grid, r, c + 1, val, dp, dir)

          "u" ->
            is_visible_dir?(grid, r - 1, c, val, dp, dir)

          "d" ->
            is_visible_dir?(grid, r + 1, c, val, dp, dir)
        end

      true ->
        false
    end
  end

  def part2(grid) do
    rows = length(grid)
    cols = hd(grid) |> length

    for r <- 1..(rows - 2), c <- 1..(cols - 2), reduce: 0 do
      max_score ->
        curr_score = get_scenic_score(grid, r, c)

        case curr_score > max_score do
          true -> curr_score
          false -> max_score
        end
    end
  end

  def get_scenic_score(grid, r, c) do
    curr = get_in(grid, [Access.at(r), Access.at(c)])
    view_dist_l = calc_dist(grid, r, c - 1, curr, "l")
    view_dist_r = calc_dist(grid, r, c + 1, curr, "r")
    view_dist_u = calc_dist(grid, r - 1, c, curr, "u")
    view_dist_d = calc_dist(grid, r + 1, c, curr, "d")

    view_dist_l * view_dist_r * view_dist_u * view_dist_d
  end

  def calc_dist(grid, r, c, val, dir) do
    curr = get_in(grid, [Access.at(r), Access.at(c)])

    cond do
      curr == nil or r < 0 or c < 0 ->
        0

      curr >= val ->
        1

      curr < val ->
        case dir do
          "l" ->
            1 + calc_dist(grid, r, c - 1, val, dir)

          "r" ->
            1 + calc_dist(grid, r, c + 1, val, dir)

          "u" ->
            1 + calc_dist(grid, r - 1, c, val, dir)

          "d" ->
            1 + calc_dist(grid, r + 1, c, val, dir)
        end
    end
  end
end
