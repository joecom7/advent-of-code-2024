NUMERICAL_KEYPAD_MAP = {
    (0, 0): "7",
    (0, 1): "8",
    (0, 2): "9",
    (1, 0): "4",
    (1, 1): "5",
    (1, 2): "6",
    (2, 0): "1",
    (2, 1): "2",
    (2, 2): "3",
    (3, 1): "0",
    (3, 2): "A",
}

NUMERICAL_KEYPAD_MAP_INVERTED = dict((v, k) for k, v in NUMERICAL_KEYPAD_MAP.items())

DIRECTIONAL_KEYPAD_MAP = {
    (0, 1): "^",
    (0, 2): "A",
    (1, 0): "<",
    (1, 1): "v",
    (1, 2): ">",
}

DIRECTIONAL_KEYPAD_MAP_INVERTED = dict(
    (v, k) for k, v in DIRECTIONAL_KEYPAD_MAP.items()
)

DIR_MAP = {
    "^": (-1, 0),
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
}

DIR_MAP_INVERTED = dict((v, k) for k, v in DIR_MAP.items())

N_MIDDLE_ROBOTS = 2
N_MIDDLE_ROBOTS_PART_TWO = 25


def add_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub_tuple(a, b):
    return (a[0] - b[0], a[1] - b[1])


def get_shortest_paths_to_press(current_letter, to_press, keymap, keymap_inverted):

    queue = []
    costs = {}

    initial_pos = keymap_inverted[current_letter]
    target_pos = keymap_inverted[to_press]

    costs[initial_pos] = 0
    queue.append(initial_pos)

    while len(queue) != 0:
        pos = queue.pop(0)
        smallest_distance = costs[pos]

        if pos == target_pos:
            break

        for dir in DIR_MAP_INVERTED:
            reached_pos = add_tuple(dir, pos)
            if reached_pos in keymap and reached_pos not in costs:
                costs[reached_pos] = smallest_distance + 1
                queue.append(reached_pos)

    # print(costs)

    return backtrack_shortest_path(target_pos, initial_pos, costs)


def backtrack_shortest_path(pos, initial_pos, costs):
    if pos == initial_pos:
        return [""]
    to_return = []
    for dir in DIR_MAP_INVERTED:
        reaching_pos = sub_tuple(pos, dir)
        if reaching_pos in costs and costs[reaching_pos] == costs[pos] - 1:
            rv = backtrack_shortest_path(reaching_pos, initial_pos, costs)
            if len(rv) != 0:
                for path in rv:
                    to_return.append(path + DIR_MAP_INVERTED[dir])
    return to_return


def get_keypad_shortest_paths(keymap, inverted_keymap):
    spmap = {}
    for letter1 in inverted_keymap:
        spmap[letter1] = {}
        for letter2 in inverted_keymap:
            spmap[letter1][letter2] = get_shortest_paths_to_press(
                letter1, letter2, keymap, inverted_keymap
            )
    return spmap


NUM_KEYPAD_SP_MAP = get_keypad_shortest_paths(
    NUMERICAL_KEYPAD_MAP, NUMERICAL_KEYPAD_MAP_INVERTED
)
DIR_KEYPAD_SP_MAP = get_keypad_shortest_paths(
    DIRECTIONAL_KEYPAD_MAP, DIRECTIONAL_KEYPAD_MAP_INVERTED
)


def get_best_move(n_robots, path, depth=0, cache={}, previous_letter="A"):
    if (n_robots, path, depth, previous_letter) in cache:
        return cache[(n_robots, path, depth, previous_letter)]
    if n_robots == depth:
        path_len = len(path)
    elif len(path) == 0:
        path_len = 0
    else:
        if depth == 0:
            relevant_keymap = NUM_KEYPAD_SP_MAP
        else:
            relevant_keymap = DIR_KEYPAD_SP_MAP
        path_len = 0
        minimum_len = -1
        letter = path[0]
        possible_paths = relevant_keymap[previous_letter][letter]
        for new_path in possible_paths:
            next_len = get_best_move(n_robots, new_path + "A", depth + 1, cache=cache)
            if minimum_len == -1 or next_len < minimum_len:
                minimum_len = next_len
        path_len += minimum_len
        previous_letter_new = letter
        path_len += get_best_move(
            n_robots, path[1:], depth, cache=cache, previous_letter=previous_letter_new
        )
    cache[(n_robots, path, depth, previous_letter)] = path_len
    return cache[(n_robots, path, depth, previous_letter)]


codes = []

with open("./21/input.txt", "r") as file:
    for line in file:
        line = line.strip()
        codes.append(line)

cache = {}

result = 0

for code in codes:
    result += get_best_move(3, code, cache=cache) * int(code[:-1])

print(f"part 1 solution: {result}")

result = 0

for code in codes:
    result += get_best_move(26, code, cache=cache) * int(code[:-1])

print(f"part 2 solution: {result}")
