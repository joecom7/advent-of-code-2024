from typing import Dict


def add_edge(n1, n2, graph):
    if n1 not in graph:
        graph[n1] = set()
    if n2 not in graph:
        graph[n2] = set()
    graph[n1].add(n2)
    graph[n2].add(n1)


def get_connected(n, graph):
    return graph[n]


def are_connected(n1, n2, graph):
    return n2 in graph[n1]


def find_loop_of_length(n, graph, length=3, depth=0, visited=set(), paths=set()):
    if all([are_connected(n, n2, graph) for n2 in visited]) or depth == 0:
        visited.add(n)
        if depth == length - 1:
            paths.add(frozenset(visited))
        else:
            for n2 in get_connected(n, graph):
                if n2 not in visited:
                    find_loop_of_length(n2, graph, length, depth + 1, visited, paths)
        visited.remove(n)
    return paths


def find_cliques(graph):
    cliques = []
    for n in graph:
        cliques.append(set([n]))
    for n in graph:
        for clique in cliques:
            if all([are_connected(n, n2, graph) for n2 in clique]):
                clique.add(n)
    return cliques


graph: Dict[str, set[str]] = {}

with open("./23/input.txt", "r") as file:
    for line in file:
        line = line.strip()
        n1 = line[:2]
        n2 = line[3:5]
        add_edge(n1, n2, graph)

all_loops = set()

for n in graph:
    if n.startswith("t"):
        all_loops.update(find_loop_of_length(n, graph, 3))

# print(all_loops)

print(f"part 1 solution: {len(all_loops)}")

# print(len(graph))

cliques = find_cliques(graph)
max_clique = max(cliques, key=lambda clique: len(clique))
max_clique = list(max_clique)
max_clique.sort()
password = ""
for node in max_clique:
    password += node + ","
password = password[:-1]
print(f"part 2 solution: {password}")