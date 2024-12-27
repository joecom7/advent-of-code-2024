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


def get_connecting(n, graph):
    connecting = set()
    for node in graph:
        if n in get_connected(node, graph):
            connecting.add(node)
    return connecting


def are_connected(n1, n2, graph):
    return n2 in graph[n1]


def eval(node, graph, visited_nodes=set(), eval_map={}):
    if node in eval_map:
        return eval_map[node]
    node_type = node[0]
    name = node[1]
    if node_type == "c":
        value = int(name)
    elif node_type == "v":
        visited_nodes.add(node)
        connected = get_connected(node, graph)
        if len(connected) != 1:
            raise Exception
        value = eval(next(iter(connected)), graph, visited_nodes, eval_map=eval_map)
    else:
        ops = get_connected(node, graph)
        if len(ops) != 2:
            raise Exception
        iterator = iter(ops)
        if node_type == "&":
            value = eval(
                next(iterator), graph, visited_nodes, eval_map=eval_map
            ) & eval(next(iterator), graph, visited_nodes, eval_map=eval_map)
        elif node_type == "|":
            value = eval(
                next(iterator), graph, visited_nodes, eval_map=eval_map
            ) | eval(next(iterator), graph, visited_nodes, eval_map=eval_map)
        elif node_type == "^":
            value = eval(
                next(iterator), graph, visited_nodes, eval_map=eval_map
            ) ^ eval(next(iterator), graph, visited_nodes, eval_map=eval_map)
        else:
            raise Exception
    eval_map[node] = value
    return eval_map[node]


def get_output_value(graph, n_bits=45):
    output = 0
    eval_map = {}
    for i in range(0, n_bits):
        z_i = ("v", f"z{str(n_bits-i).zfill(2)}")
        output += eval(z_i, graph, eval_map=eval_map) << n_bits - i
    return output


def substitute_node(n_old, n_new, graph):
    connected = graph[n_old]
    graph[n_old] = set()
    graph[n_new] = connected
    for n in get_connecting(n_old, graph):
        graph[n].remove(n_old)
        graph[n].add(n_new)


def swap_nodes(a, b, graph):
    connected_a = get_connected(a, graph)
    connected_b = get_connected(b, graph)
    graph[b] = connected_a
    graph[a] = connected_b


def check_formula_correct(graph, index):
    if index == 0:
        # first bit, no c_in
        x_i = ("v", f"x{str(index).zfill(2)}")
        y_i = ("v", f"y{str(index).zfill(2)}")
        z_i = ("v", f"z{str(index).zfill(2)}")
        if len(get_connected(z_i, graph)) != 1:
            return False
        xor_gate = next(iter(get_connected(z_i, graph)))
        if xor_gate[0] != "^":
            return False
        if get_connected(xor_gate, graph) != set([x_i, y_i]):
            return False
        found_c_out = False
        for gate in get_connecting(x_i, graph):
            if get_connected(gate, graph) == set([x_i, y_i]) and gate[0] == "&":
                found_c_out = True
                substitute_node(
                    next(iter(get_connecting(gate, graph))), ("v", "cout0"), graph
                )
        return found_c_out
    else:
        # other bit, there is c_in
        x_i = ("v", f"x{str(index).zfill(2)}")
        y_i = ("v", f"y{str(index).zfill(2)}")
        z_i = ("v", f"z{str(index).zfill(2)}")
        c_in = ("v", f"cout{index-1}")

        found_xixoryi = False
        found_xiandyi = False

        # find xixoryi and xiandyi
        for gate in get_connecting(x_i, graph):
            if gate[0] == "^" and get_connected(gate, graph) == set([x_i, y_i]):
                found_xixoryi = True
                xixoryi = next(iter(get_connecting(gate, graph)))
                substitute_node(xixoryi, ("v", f"x{index}^y{index}"), graph)
            elif gate[0] == "&" and get_connected(gate, graph) == set([x_i, y_i]):
                found_xiandyi = True
                xixoryi = next(iter(get_connecting(gate, graph)))
                substitute_node(xixoryi, ("v", f"x{index}&y{index}"), graph)
            else:
                return False

        if (not found_xiandyi) or (not found_xixoryi):
            return False

        xixoryi = ("v", f"x{index}^y{index}")
        xiandyi = ("v", f"x{index}&y{index}")

        # check if zi = (xi xor yi) xor cin
        if len(get_connected(z_i, graph)) != 1:
            return False
        xor_gate = next(iter(get_connected(z_i, graph)))
        if xor_gate[0] != "^":
            return False
        if get_connected(xor_gate, graph) != set([c_in, xixoryi]):
            return False

        # find (xi xor yi) and cin
        to_check = get_connecting(xixoryi, graph) - set([xor_gate])
        if len(to_check) != 1:
            return False
        xixoryiandcin = next(iter(to_check))
        if xixoryiandcin[0] != "&":
            return False
        if get_connected(xixoryiandcin, graph) != set([c_in, xixoryi]):
            return False
        xixoryiandcin = next(iter(get_connecting(xixoryiandcin, graph)))
        orgateset = get_connecting(xixoryiandcin, graph)
        if len(orgateset) != 1:
            return False
        orgate = next(iter(orgateset))
        if get_connected(orgate, graph) != set([xixoryiandcin, xiandyi]):
            return False
        if len(get_connecting(orgate, graph)) != 1:
            return False
        substitute_node(
            next(iter(get_connecting(orgate, graph))), ("v", f"cout{index}"), graph
        )

        return True


def remove_edges(n, graph):
    graph[n] = set()


def set_x_bit(index, value, graph):
    x_i = ("v", f"x{str(index).zfill(2)}")
    remove_edges(x_i, graph)
    add_edge(x_i, ("c", value), graph)


def set_y_bit(index, value, graph):
    y_i = ("v", f"y{str(index).zfill(2)}")
    remove_edges(y_i, graph)
    add_edge(y_i, ("c", value), graph)


def to_bits(x, bits=5):
    return [i for i in bin(x)[2:].zfill(bits)]


def set_x_value(x, graph, n_bits=45):
    x_bin = bin(x)[2:].zfill(n_bits)
    for i in range(0, n_bits):
        set_x_bit(n_bits - i - 1, x_bin[i], graph)


def set_y_value(y, graph, n_bits=45):
    y_bin = bin(y)[2:].zfill(n_bits)
    for i in range(0, n_bits):
        set_y_bit(n_bits - i - 1, y_bin[i], graph)


def fix_bit(n_bit, graph):
    # this function assumes that bits 0 to n_bit - 1 are correct

    z_i = ("v", f"z{str(n_bit).zfill(2)}")

    visited_nodes = set()
    eval_map = {}
    eval(z_i, graph, visited_nodes)

    for i in [0, 1]:
        for j in [0, 1]:
            x = i << n_bit
            set_x_value(x, graph)
            y = j << n_bit
            set_y_value(y, graph)
            if eval(z_i, graph, eval_map=eval_map) != i ^ j:
                print("error")


graph: Dict[tuple[str, str], set[tuple[str, str]]] = {}

with open("./24/input.txt", "r") as file:
    data = file.read()

    matches = re.findall(pattern_iv, data)

    for match in matches:

        node_var = ("v", match[0])
        node_const = ("c", match[1])
        add_edge(node_var, node_const, graph)

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
print(f"part 1 solution: {get_output_value(graph)}")

# i found them by manually swapping sus wires
to_swap = ["dkr", "z05", "htp", "z15", "hhh", "z20", "ggk", "rhv"]

for i in range(0, len(to_swap) // 2):
    swap_nodes(("v", to_swap[2 * i]), ("v", to_swap[2 * i + 1]), graph)

for i in range(0, 45):
    if not check_formula_correct(graph, i):
        print(f"formula incorrect for bit {i}")

output = ""
to_swap.sort()
for string in to_swap:
    output += string + ","
print(f"part 2 solution: {output[:-1]}")
