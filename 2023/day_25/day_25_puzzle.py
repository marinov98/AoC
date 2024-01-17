import networkx as nx


def solution_helper(input_file: str):
    graph = nx.Graph()
    with open(input_file, "r") as file:
        for line in file:
            left, right = line.split(":")
            for node in right.strip().split():
                graph.add_edge(left, node)
                graph.add_edge(node, left)

    graph.remove_edges_from(nx.minimum_edge_cut(graph))
    answer_left, answer_right = nx.connected_components(graph)

    return len(answer_left) * len(answer_right)


def solution(inputs: list[str]):
    for input_file in inputs:
        answer = solution_helper(input_file)
        print(f"Answer using input file '{input_file}' ", answer)


if __name__ == "__main__":
    solution(
        [
            "test.txt",
            "day_25_puzzle_input.txt"
        ]
    )
