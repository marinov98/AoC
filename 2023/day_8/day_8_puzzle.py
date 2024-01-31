from math import lcm
def solution(input_file: str) -> None:
    inputs = {}
    starters = []
    with open(input_file) as file:
        for line in file:
            inputs, starters = get_inputs(line.strip(), inputs, starters)
    # print(f"{input_file} Answer to the first problem should be:", navigate_map(inputs))
    print(f"{input_file} Answer to the second problem should be:", find_ways(inputs, starters))

def get_inputs(input_line: str, inputs: dict, starters: list) -> tuple:
    if "=" not in input_line and ("R" in input_line or "L" in input_line):
        inputs['instructions'] = input_line
    else:

        element = input_line[:3]
        if len(element) > 0:
            if element.endswith("A"):
                starters.append(element)
            input_split = input_line.split(" = ")
            nav_nodes = input_split[1].split(", ")
            inputs[element] = [nav_nodes[0][1:4], nav_nodes[1][:3]]

    return inputs, starters

def navigate_map(inputs: dict, initial_node: str = "AAA") -> int:
    steps = 0
    curr_node = initial_node
    instructions = inputs['instructions']
    instructions_size = len(instructions)
    instruction_i = 0
    while curr_node != "ZZZ":
        if instructions[instruction_i] == "L":
            curr_node = inputs[curr_node][0]
        else:
            curr_node = inputs[curr_node][1]
        steps +=1
        instruction_i = (instructions + 1) % instructions_size

    return steps

def find_ways(inputs: dict, starters: list):
    steps = 0
    curr_nodes = [start_node for start_node in starters]
    cache = {}
    instructions = inputs['instructions']
    instructions_size = len(instructions)
    total_nodes = len(starters)
    answer = 1
    instruction_i = 0
    nodes_finished = 0
    while nodes_finished != total_nodes:
        if instructions[instruction_i] == "L":
            curr_nodes = [inputs[curr_node][0] for curr_node in curr_nodes]
        else:
            curr_nodes = [inputs[curr_node][1] for curr_node in curr_nodes]
        steps +=1
        instruction_i =  (instruction_i + 1) % instructions_size
        for node in curr_nodes:
            if node.endswith("Z"):
                if node not in cache:
                    cache[node] = steps
                    nodes_finished += 1
                    answer = lcm(answer, steps)
        if total_nodes - nodes_finished != len(curr_nodes):
            curr_nodes = list(filter(lambda x: x not in cache, curr_nodes))
                    
    return answer

if __name__ == "__main__":
    # solution("test.txt")
    # solution("test2.txt")
    solution("day_8_puzzle_input.txt")
