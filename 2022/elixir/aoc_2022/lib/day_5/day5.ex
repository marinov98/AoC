defmodule Day5 do
  @inputs ["lib/day_5/test.txt", "lib/day_5/day5input.txt"]

  def solution() do
    @inputs
    |> Enum.map(&solution_helper/1)
  end

  def solution_helper(input_file) do
    input =
      input_file
      |> File.read!()
      |> String.split("\n\n", trim: true)
      |> construct_from_input

    {part1(input), 0}
  end

  def construct_from_input(input) do
    stacks =
      List.first(input)
      |> String.split("\n", trim: true)
      |> Enum.reduce(%{}, fn elem, acc ->
        curr_list = elem |> String.split(" ")
        [id | stack] = curr_list
        Map.put(acc, String.to_integer(id), stack)
      end)

    instructions =
      List.last(input)
      |> String.split("\n", trim: true)
      |> Enum.map(fn elem ->
        elem
        |> String.split(" ")
        |> Enum.filter(&(&1 != "move" and &1 != "from" and &1 != "to"))
        |> Enum.map(&String.to_integer/1)
        |> List.to_tuple()
      end)

    {stacks, instructions}
  end

  def format_result(res_map) do
    res_map
    |> Map.to_list()
    |> Enum.filter(fn elem ->
      {_, stack} = elem

      case stack do
        [] -> false
        _ -> true
      end
    end)
    |> Enum.map(fn elem ->
      {_, stack} = elem
      List.last(stack)
    end)
    |> Enum.join()
  end

  def part1(input) do
    {stack_map, instructions} = input

    simulation(stack_map, instructions, &part1_utility/3)
    |> format_result
  end

  def simulation(stack_map, instructions, utility_fn) do
    case instructions do
      [] ->
        stack_map

      _ ->
        [curr_instruction | rest] = instructions
        stack_map = utility_fn.(stack_map, curr_instruction, 1)
        simulation(stack_map, rest, utility_fn)
    end
  end

  def part1_utility(stack_map, curr_instruction, curr_move) do
    {move, from, to} = curr_instruction

    cond do
      move < curr_move ->
        stack_map

      true ->
        from_stack = Map.get(stack_map, from)
        to_stack = Map.get(stack_map, to)
        {elem, new_from_stack} = List.pop_at(from_stack, -1)
        new_to_stack = List.insert_at(to_stack, -1, elem)
        stack_map = Map.update(stack_map, from, [], fn _ -> new_from_stack end)
        stack_map = Map.update(stack_map, to, [], fn _ -> new_to_stack end)
        part1_utility(stack_map, curr_instruction, curr_move + 1)
    end
  end
end
