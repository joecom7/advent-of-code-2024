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

BACKTRACKING_MAP_REVERSED = dict((v, k) for k, v in DIR_MAP.items())
N_MIDDLE_ROBOTS = 2
N_MIDDLE_ROBOTS_PART_TWO = 10


class OutOfKeypadException(Exception):
    pass


def add_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub_tuple(a, b):
    return (a[0] - b[0], a[1] - b[1])


def get_possible_configs(is_last_robot=True):
    configs = []
    for p1 in DIRECTIONAL_KEYPAD_MAP.keys():
        if is_last_robot:
            keyset = NUMERICAL_KEYPAD_MAP.keys()
        else:
            keyset = DIRECTIONAL_KEYPAD_MAP.keys()
        for p2 in keyset:
            configs.append((p1, p2))
    return tuple(configs)


def get_reached_config(move, robots_config, is_last_robot=True):

    current_move = move
    middle_robot_config = robots_config[0]
    robot_config = robots_config[1]

    if current_move in DIR_MAP:
        dir_to_move = DIR_MAP[current_move]
        middle_robot_config = add_tuple(middle_robot_config, dir_to_move)
        if middle_robot_config not in DIRECTIONAL_KEYPAD_MAP:
            raise OutOfKeypadException()
        current_move = "_"
    elif current_move == "A":
        current_move = DIRECTIONAL_KEYPAD_MAP[middle_robot_config]

    if current_move in DIR_MAP:
        dir_to_move = DIR_MAP[current_move]
        robot_config = add_tuple(robot_config, dir_to_move)
        if is_last_robot and robot_config not in NUMERICAL_KEYPAD_MAP:
            raise OutOfKeypadException()
        elif not is_last_robot and robot_config not in DIRECTIONAL_KEYPAD_MAP:
            raise OutOfKeypadException()

    return middle_robot_config, robot_config


def get_reaching_config(move, robots_config, is_last_robot=True):

    current_move = move
    middle_robot_config = robots_config[0]
    robot_config = robots_config[1]

    if current_move in DIR_MAP:
        dir_to_move = DIR_MAP[current_move]
        middle_robot_config = sub_tuple(middle_robot_config, dir_to_move)
        if middle_robot_config not in DIRECTIONAL_KEYPAD_MAP:
            raise OutOfKeypadException()
        current_move = "_"
    elif current_move == "A":
        current_move = DIRECTIONAL_KEYPAD_MAP[middle_robot_config]

    if current_move in DIR_MAP:
        dir_to_move = DIR_MAP[current_move]
        robot_config = sub_tuple(robot_config, dir_to_move)
        if is_last_robot and robot_config not in NUMERICAL_KEYPAD_MAP:
            raise OutOfKeypadException()
        elif not is_last_robot and robot_config not in DIRECTIONAL_KEYPAD_MAP:
            raise OutOfKeypadException()

    return middle_robot_config, robot_config


def bfs_robot(pos, target_pos, is_last_robot=True, is_first_robot=False):
    queue = []
    costs = {}

    middle_robot_pos = DIRECTIONAL_KEYPAD_MAP_INVERTED["A"]
    initial_config = (middle_robot_pos, pos)
    target_config = (middle_robot_pos, target_pos)

    for config in get_possible_configs(is_last_robot):
        if config == initial_config:
            costs[config] = 0
        else:
            costs[config] = float("inf")

    queue.append(initial_config)

    while len(queue) != 0:
        config = queue.pop(0)
        smallest_distance = costs[config]

        if config == target_config:
            break

        for move in DIRECTIONAL_KEYPAD_MAP_INVERTED.keys():
            try:
                reached_config = get_reached_config(move, config, is_last_robot)
                if costs[reached_config] == float("inf"):
                    costs[reached_config] = smallest_distance + 1
                    queue.append(reached_config)
            except OutOfKeypadException:
                pass

    # backtracking

    path, _ = backtrack(
        target_config, initial_config, costs, is_last_robot, is_first_robot
    )

    return path + "A"


def backtrack(config, start_config, costs, is_last_robot, is_first_robot):
    if config == start_config:
        return "", True
    for move in DIRECTIONAL_KEYPAD_MAP_INVERTED.keys():
        try:
            reaching = get_reaching_config(move, config, is_last_robot)
            if costs[reaching] == costs[config] - 1:
                rv = backtrack(
                    reaching, start_config, costs, is_last_robot, is_first_robot
                )
                if rv[1]:
                    if not is_first_robot:
                        if move == "A":
                            return rv[0] + DIRECTIONAL_KEYPAD_MAP[config[0]], True
                        else:
                            return rv[0], True
                    else:
                        return rv[0] + move, True
        except OutOfKeypadException:
            pass
    return "", False


def get_shortest_path_for_code(code, n_middle_robots):
    path = ""
    previous_letter = "A"
    for letter in code:
        path += get_shortest_path_for_letter_recursive(
            previous_letter, letter, n_middle_robots
        )
        previous_letter = letter
    return path


def get_shortest_path_for_letter_recursive(
    previous_letter, letter, n_middle_robots, depth=0
):
    if n_middle_robots == depth:
        return letter
    if depth == 0:
        relevant_map = NUMERICAL_KEYPAD_MAP_INVERTED
    else:
        relevant_map = DIRECTIONAL_KEYPAD_MAP_INVERTED
    last_robot_pos = relevant_map[previous_letter]
    target_pos = relevant_map[letter]
    path = ""
    previous_letter = "A"
    for letter in bfs_robot(
        last_robot_pos, target_pos, (depth == 0), (depth + 1 == n_middle_robots)
    ):
        path += get_shortest_path_for_letter_recursive(
            previous_letter, letter, n_middle_robots, depth + 1
        )
        previous_letter = letter
    return path


codes = []

with open("./21/input.txt", "r") as file:
    for line in file:
        line = line.strip()
        codes.append(line)

# print(codes)

total_complexity = 0

for code in codes:
    print(get_shortest_path_for_code(code, 2))

# print(f"part 1 solution: {total_complexity}")
