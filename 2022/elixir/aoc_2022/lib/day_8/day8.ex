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
        {is_visible, dp} = visible?(grid, r, c, dp)

        case is_visible do
          true -> {num_visible + 1, dp}
          false -> {num_visible, dp}
        end
    end
    |> elem(0)
  end

  defp visible?(grid, r, c, dp) do
    curr = get_in(grid, [Access.at(r), Access.at(c)])

    cond do
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

    for r <- 1..(rows - 2), c <- 1..(cols - 2), reduce: {0, %{}} do
      {curr_max_score, dp} ->
        {new_score, dp} = get_scenic_score(grid, r, c, dp)
        {max(curr_max_score, new_score), dp}
    end
    |> elem(0)
  end

  defp get_scenic_score(grid, r, c, dp) do
    curr = get_in(grid, [Access.at(r), Access.at(c)])
    view_dist_l = calc_dist(grid, r, c - 1, curr, "l", dp)
    dp = Map.put(dp, {r, c, "l"}, view_dist_l)
    view_dist_r = calc_dist(grid, r, c + 1, curr, "r", dp)
    dp = Map.put(dp, {r, c, "r"}, view_dist_r)
    view_dist_u = calc_dist(grid, r - 1, c, curr, "u", dp)
    dp = Map.put(dp, {r, c, "u"}, view_dist_u)
    view_dist_d = calc_dist(grid, r + 1, c, curr, "d", dp)
    dp = Map.put(dp, {r, c, "d"}, view_dist_d)

    {view_dist_l * view_dist_r * view_dist_d * view_dist_u, dp}
  end

  defp calc_dist(grid, r, c, val, dir, dp) do
    curr = get_in(grid, [Access.at(r), Access.at(c)])

    cond do
      curr == nil ->
        0

      curr >= val or r == 0 or c == 0 or r == length(grid) - 1 or c == length(hd(grid)) - 1 ->
        1

      curr < val ->
        pre_computed_dist = Map.get(dp, {r, c, dir}, 1)

        case dir do
          "l" ->
            pre_computed_dist + calc_dist(grid, r, c - pre_computed_dist, val, dir, dp)

          "r" ->
            pre_computed_dist + calc_dist(grid, r, c + pre_computed_dist, val, dir, dp)

          "u" ->
            pre_computed_dist + calc_dist(grid, r - pre_computed_dist, c, val, dir, dp)

          "d" ->
            pre_computed_dist + calc_dist(grid, r + pre_computed_dist, c, val, dir, dp)
        end
    end
  end
end
