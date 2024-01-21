defmodule Day7 do
  @inputs ["lib/day_7/test.txt", "lib/day_7/day7input.txt"]
  # @inputs ["lib/day_7/test.txt"]

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
    |> Enum.flat_map(fn {_, v} -> 
      case v < 100001 do
        true -> [v]
        false -> []
      end
    end)
    |> Enum.sum()
  end

  defp part1_utility(input, curr_line, path \\ [], curr_dir \\ "", size_tracker \\ %{}, children_tracker \\ %{}, file_name_tracker \\ %{}) do
    case input do
      [] -> 
        size_tracker
      _ ->
      split = String.split(curr_line, " ")
      [_ | next_lines ] = input
      case hd(split) do
        "$" -> # command
          [_ | rest ] = split
          case List.first(rest) do
            "cd" -> # going into new directory
              next_dir = List.last(rest)
              case curr_dir do
                "" -> # should be first command
                  children_tracker = Map.put(children_tracker, next_dir, MapSet.new())
                  path = [next_dir]
                  size_tracker = Map.put(size_tracker, Enum.join(path), 0)
                  part1_utility(next_lines, List.first(next_lines), path, next_dir, size_tracker, children_tracker, file_name_tracker)
                _ -> 
                    case next_dir do
                      ".." -> 
                          [prev_dir | remaining_path] = path
                          part1_utility(next_lines, List.first(next_lines), remaining_path, prev_dir, size_tracker, children_tracker, file_name_tracker)
                      _ ->
                        part1_utility(next_lines, List.first(next_lines), [next_dir | path], next_dir, size_tracker, children_tracker, file_name_tracker)
                    end
              end
              "ls" -> 
                  part1_utility(next_lines, List.first(next_lines), path, curr_dir, size_tracker, children_tracker, file_name_tracker)
          end
        "dir" -> # dir
            part1_utility(next_lines, List.first(next_lines), path, curr_dir, size_tracker, children_tracker, file_name_tracker)
        _ -> # size
            file_name = List.last(split)
            curr_files = Map.get(file_name_tracker, Enum.join(path), MapSet.new())
            case  MapSet.member?(curr_files, file_name) do
              false -> 
                val = String.to_integer(List.first(split))
                curr_files = MapSet.put(curr_files, file_name)
                file_name_tracker = Map.put(file_name_tracker, Enum.join(path), curr_files)
                size_tracker = Map.update(size_tracker, Enum.join(path), val, &(&1 + val))
                size_tracker = update_parents(path, size_tracker, val)
                part1_utility(next_lines, List.first(next_lines), path, curr_dir, size_tracker, children_tracker, file_name_tracker)
              true ->
                part1_utility(next_lines, List.first(next_lines), path, curr_dir, size_tracker, children_tracker, file_name_tracker)
            end
      end
    end
  end

  defp update_parents(path, size_tracker, val) do
    [_ | rest] = path
    case rest do
       [] -> 
        size_tracker
       _ ->
        size_tracker = Map.update(size_tracker, Enum.join(rest), val, &(&1 + val))
        update_parents(rest, size_tracker, val)
    end
  end

  def part2(input) do
    input
    |> part1_utility(List.first(input))
    |> part2_utility()
  end
  defp part2_utility(size_tracker) do
    maximum = 70000000
    minimum = 30000000
    curr_size = 70000000 - Map.get(size_tracker, "/")
    IO.inspect(curr_size)
    size_tracker
    |> Enum.reduce({0, maximum}, fn {_ , v}, {val, diff} -> 
        case curr_size + v >= minimum do
          true ->
            if curr_size + v < diff do
              {v, curr_size + v}
            else 
              {val, diff}
            end
          false ->
            {val , diff}
          end
    end)
    |> elem(0)
  end
end
