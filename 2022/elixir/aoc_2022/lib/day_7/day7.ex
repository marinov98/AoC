defmodule Day7 do
  # @inputs ["lib/day_7/test.txt", "lib/day_7/day7input.txt"]
  @inputs ["lib/day_7/test.txt"]

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

  def part1(input) do
    input
    |> part1_utility(List.first(input))
  end

  def part1_utility(input, curr_line, parent_tracker \\ %{}, curr_dir \\ "", size_tracker \\ %{}, children_tracker \\ %{}, file_name_tracker \\ %{}) do
    case input do
      [] -> {size_tracker, children_tracker}
      _ ->
      split = String.split(curr_line, " ")
      [_ | next_lines ] = input
      case hd(split) do
        "$" -> # command
          [_ | rest ] = split
          next_dir = List.last(rest)
          case List.first(rest) do
            "cd" -> # going into new directory
              case curr_dir do
                "" -> # should be first command
                  children_tracker = Map.put(children_tracker, next_dir, MapSet.new())
                  size_tracker = Map.put(size_tracker, next_dir, 0)
                  # parent_tracker = Map.put(parent_tracker, next_dir, curr_dir)
                  [_ | next_lines ] = input
                  part1_utility(next_lines, List.first(next_lines), parent_tracker, next_dir, size_tracker, children_tracker, file_name_tracker)
                _ -> 
                    case next_dir do
                      ".." -> 
                          prev_dir = Map.get(parent_tracker, curr_dir)
                          part1_utility(next_lines, List.first(next_lines), parent_tracker, prev_dir, size_tracker, children_tracker, file_name_tracker)
                      _ ->
                      case Map.get(children_tracker, next_dir) do
                        nil -> 
                          children_tracker = Map.put(children_tracker, next_dir, MapSet.new())
                          size_tracker = Map.put(size_tracker, next_dir, 0)
                          parent_tracker = Map.put(parent_tracker, next_dir, curr_dir)
                          part1_utility(next_lines, List.first(next_lines), parent_tracker, next_dir, size_tracker, children_tracker, file_name_tracker)
                        _ -> 
                          part1_utility(next_lines, List.first(next_lines), parent_tracker, next_dir, size_tracker, children_tracker, file_name_tracker)
                      end
                    end
              end
              "ls" -> 
                  part1_utility(next_lines, List.first(next_lines), parent_tracker, curr_dir, size_tracker, children_tracker, file_name_tracker)
          end
        "dir" -> # dir
          [_ | rest ] = split
          next_dir = List.last(rest)
          curr_dir_children = Map.get(children_tracker, curr_dir)
          case MapSet.member?(curr_dir_children, next_dir) do
              false ->
                curr_dir_children = MapSet.put(curr_dir_children, next_dir)
                children_tracker = Map.put(children_tracker, curr_dir, curr_dir_children)
                part1_utility(next_lines, List.first(next_lines), parent_tracker, curr_dir, size_tracker, children_tracker, file_name_tracker)
              true ->
                part1_utility(next_lines, List.first(next_lines), parent_tracker, curr_dir, size_tracker, children_tracker, file_name_tracker)
          end
        _ -> # size
            file_name = List.last(split)
            curr_files = Map.get(file_name_tracker, curr_dir, MapSet.new())
            case  MapSet.member?(curr_files, file_name) do
              false -> 
                val = String.to_integer(List.first(split))
                curr_files = MapSet.put(curr_files, file_name)
                file_name_tracker = Map.put(file_name_tracker, curr_dir, curr_files)
                size_tracker = Map.update(size_tracker, curr_dir, val, &(&1 + val))
                size_tracker = update_parents(parent_tracker, size_tracker, curr_dir, val)
                part1_utility(next_lines, List.first(next_lines), parent_tracker, curr_dir, size_tracker, children_tracker, file_name_tracker)
              true ->
                part1_utility(next_lines, List.first(next_lines), parent_tracker, curr_dir, size_tracker, children_tracker, file_name_tracker)
            end
      end
    end
  end

  def part2(input) do
    input
  end

  def update_parents(parent_tracker, size_tracker, curr, val) do
    parent_dir = Map.get(parent_tracker, curr)
    case parent_dir do
      nil ->
        size_tracker
      _ -> 
        size_tracker = Map.update(size_tracker, parent_dir, val, &(&1 + val))
        update_parents(parent_tracker, size_tracker, parent_dir, val)
    end
  end
end
