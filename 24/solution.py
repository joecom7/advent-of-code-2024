import re
from typing import Dict
import networkx as nx

pattern_iv = r"(.+):\ ([0,1])"
pattern_op = r"(.+)\ (XOR|AND|OR)\ (.+)\ ->\ (.+)"


def add_edge(n1, n2, graph):
    if n1 not in graph:
        graph[n1] = set()
    if n2 not in graph:
        graph[n2] = set()
    graph[n1].add(n2)


def remove_edges(n, graph):
    graph[n] = set()


def get_connected(n, graph):
    return graph[n]


def are_connected(n1, n2, graph):
    return n2 in graph[n1]


def to_bits(x, bits=5):
    return [i for i in bin(x)[2:].zfill(bits)]


def try_circuit(x, y, x_eqnodes, y_eqnodes, graph):
    x_bits = to_bits(x,len(x_eqnodes))
    y_bits = to_bits(y,len(y_eqnodes))
    for (node,bit) in zip(x_eqnodes,x_bits):
        remove_edges(node, graph)
        node_const = ("c", bit)
        add_edge(node, node_const, graph)
    for (node,bit) in zip(y_eqnodes,y_bits):
        remove_edges(node, graph)
        node_const = ("c", bit)
        add_edge(node, node_const, graph)
    eval_map = {}
    return get_values_starting_with("z", graph, eval_map)


def eval(node, graph, eval_map={}):
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
        value = eval(next(iter(connected)), graph, eval_map)
    elif node_type == "=":
        connected = get_connected(node, graph)
        if len(connected) != 1:
            raise Exception
        value = eval(next(iter(connected)), graph, eval_map)
    else:
        ops = get_connected(node, graph)
        if len(ops) != 2:
            raise Exception
        iterator = iter(ops)
        if node_type == "&":
            value = eval(next(iterator), graph, eval_map) & eval(
                next(iterator), graph, eval_map
            )
        elif node_type == "|":
            value = eval(next(iterator), graph, eval_map) | eval(
                next(iterator), graph, eval_map
            )
        elif node_type == "^":
            value = eval(next(iterator), graph, eval_map) ^ eval(
                next(iterator), graph, eval_map
            )
        else:
            raise Exception
    eval_map[node] = value
    return eval_map[node]


def get_values_starting_with(
    prefix, graph: Dict[tuple[str, str], set[tuple[str, str]]],eval_map={}
):
    nodes = list(graph.keys())
    nodes.sort(key=lambda node: node[1], reverse=True)
    output = ""
    for node in nodes:
        if node[0] == "v" and node[1].startswith(prefix):
            output += str(eval(node, graph,eval_map))
    return int(output, 2)


graph: Dict[tuple[str, str], set[tuple[str, str]]] = {}

with open("./24/input.txt", "r") as file:
    data = file.read()

    matches = re.findall(pattern_iv, data)

    for match in matches:

        node_var = ("v", match[0])
        node_const = ("c", match[1])
        node_op = ("=", "="+match[0] + match[1])
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
        node_op = (op, op+match[2] + match[3])
        node_v1 = ("v", match[0])
        node_v2 = ("v", match[2])
        add_edge(node_result, node_op, graph)
        add_edge(node_op, node_v1, graph)
        add_edge(node_op, node_v2, graph)

# print(graph)
print(get_values_starting_with("z", graph))
# print(try_circuit(0, 1, graph))

x_eqnodes = []
y_eqnodes = []

nodes = list(graph.keys())
nodes.sort(key=lambda node: node[1], reverse=True)
for node in nodes:
    if node[0] == "v" and node[1].startswith("x"):
        node_eq = next(iter(get_connected(node, graph)))
        x_eqnodes.append(node_eq)
    elif node[0] == "v" and node[1].startswith("y"):
        node_eq = next(iter(get_connected(node, graph)))
        y_eqnodes.append(node_eq)

#print(try_circuit(11, 13, x_eqnodes, y_eqnodes, graph))

G = nx.Graph(graph)
nx.draw(G)