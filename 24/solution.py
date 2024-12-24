import re
from typing import Dict

pattern_iv = r"(.+):\ ([0,1])"
pattern_op = r"(.+)\ (XOR|AND|OR)\ (.+)\ ->\ (.+)"


def add_edge(n1, n2, graph):
    if n1 not in graph:
        graph[n1] = set()
    if n2 not in graph:
        graph[n2] = set()
    graph[n1].add(n2)


def get_connected(n, graph):
    return graph[n]


def are_connected(n1, n2, graph):
    return n2 in graph[n1]


eval_map = {}


def eval(node, graph):
    if node in eval_map:
        return eval_map[node]
    node_type = node[0]
    name = node[1]
    if node_type == "c":
        value = int(name)
    elif node_type == "v":
        connected = get_connected(node, graph)
        if len(connected) != 1:
            raise Exception
        value = eval(next(iter(connected)), graph)
    elif node_type == "=":
        connected = get_connected(node, graph)
        if len(connected) != 1:
            raise Exception
        value = eval(next(iter(connected)), graph)
    else:
        ops = get_connected(node, graph)
        if len(ops) != 2:
            raise Exception
        iterator = iter(ops)
        if node_type == "&":
            value = eval(next(iterator), graph) & eval(next(iterator), graph)
        elif node_type == "|":
            value = eval(next(iterator), graph) | eval(next(iterator), graph)
        elif node_type == "^":
            value = eval(next(iterator), graph) ^ eval(next(iterator), graph)
        else:
            raise Exception
    eval_map[node] = value
    return eval_map[node]

def get_values_starting_with(prefix,graph: Dict[tuple[str, str], set[tuple[str, str]]]):
    nodes = list(graph.keys())
    nodes.sort(key=lambda node:node[1],reverse=True)
    output = ""
    for node in nodes:
        if node[0] == "v" and node[1].startswith(prefix):
            output += str(eval(node,graph))
    return int(output,2)

graph: Dict[tuple[str, str], set[tuple[str, str]]] = {}

with open("./24/input.txt", "r") as file:
    data = file.read()

    matches = re.findall(pattern_iv, data)

    for match in matches:

        node_var = ("v", match[0])
        node_const = ("c", match[1])
        node_op = ("=", match[0] + match[1])
        add_edge(node_var, node_op, graph)
        add_edge(node_op, node_const, graph)

    matches = re.findall(pattern_op, data)

    for match in matches:

        node_result = ("v", match[3])
        if match[1] == "AND":
            op = "&"
        elif match[1] == "OR":
            op = "|"
        elif match[1] == "XOR":
            op = "^"
        node_op = (op, match[2] + match[3])
        node_v1 = ("v", match[0])
        node_v2 = ("v", match[2])
        add_edge(node_result, node_op, graph)
        add_edge(node_op, node_v1, graph)
        add_edge(node_op, node_v2, graph)

# print(graph)
print(get_values_starting_with("z",graph))
