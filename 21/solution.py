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

DIRECTIONAL_KEYPAD_MAP_INVERTED = dict((v, k) for k, v in DIRECTIONAL_KEYPAD_MAP.items())

DIR_MAP = {
    "^": (-1, 0),
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
}

N_MIDDLE_ROBOTS = 2

class OutOfKeypadException(Exception):
    pass


def add_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])


def get_reached_config(move, current_config):
    middle_robot_configs = current_config[0]
    last_robot_config = current_config[1]
    new_middle_robot_configs = []
    pressed_last = False

    current_move = move
    for middle_robot_config in middle_robot_configs:
        if current_move in DIR_MAP:
            dir_to_move = DIR_MAP[current_move]
            middle_robot_config = add_tuple(middle_robot_config, dir_to_move)
            if middle_robot_config not in DIRECTIONAL_KEYPAD_MAP:
                raise OutOfKeypadException()
            current_move = "_"
        elif current_move == "A":
            current_move = DIRECTIONAL_KEYPAD_MAP[middle_robot_config]
        new_middle_robot_configs.append(middle_robot_config)

    if current_move in DIR_MAP:
        dir_to_move = DIR_MAP[current_move]
        last_robot_config = add_tuple(last_robot_config, dir_to_move)
        if last_robot_config not in NUMERICAL_KEYPAD_MAP:
            raise OutOfKeypadException()
    #elif current_move == "A":
    #    pressed_last = True
    return tuple(new_middle_robot_configs), last_robot_config


def get_possible_configs(n_middle_robots, depth=0):
    if depth == n_middle_robots:
        empty_tuple = ()
        return tuple([(empty_tuple, button) for button in NUMERICAL_KEYPAD_MAP.keys()])
    recursive_output = get_possible_configs(n_middle_robots, depth + 1)
    possible_configs = []
    for config in recursive_output:
        for current_config in DIRECTIONAL_KEYPAD_MAP.keys():
            new_config = [current_config]
            new_config.extend(config[0])
            possible_configs.append(tuple([tuple(new_config), config[1]]))
    return tuple(possible_configs)

def get_base_config(n_middle_robots,last_robot_pos):
    middle_robots_poses = []
    for _ in range(0,n_middle_robots):
        middle_robots_poses.append(DIRECTIONAL_KEYPAD_MAP_INVERTED['A'])
    return tuple([tuple(middle_robots_poses),last_robot_pos])

def get_shortest_path_to_press(current_config, to_press):

    queue = []
    costs = {}

    middle_robot_configs = current_config[0]
    last_robot_config = current_config[1]
    n_middle_robots = len(middle_robot_configs)
    to_reach = get_base_config(n_middle_robots,NUMERICAL_KEYPAD_MAP_INVERTED[to_press])

    # for j in range(0, n_rows):
    #    for i in range(0, n_cols):
    #        if board[(j, i)] != "#":
    #            if (j, i) == start:
    #                costs[(j, i)] = 0
    #            else:
    #                costs[(j, i)] = float("inf")

    for config in get_possible_configs(n_middle_robots):
        if config == current_config:
            costs[config] = 0
        else:
            costs[config] = float("inf")

    queue.append(current_config)

    while len(queue) != 0:
        config = queue.pop(0)
        smallest_distance = costs[config]

        if config == to_reach:
            break
                    
        for move in DIRECTIONAL_KEYPAD_MAP_INVERTED.keys():
            try:
                reached_config = get_reached_config(move,config)
                if costs[reached_config] == float('inf'):
                    costs[reached_config] = smallest_distance + 1
                    queue.append(reached_config)
            except OutOfKeypadException:
                pass

    # print(costs)

    return costs[to_reach] + 1

def get_shortest_path_for_code(code,n_middle_robots):
    shortest_path = 0
    current_config = (get_base_config(n_middle_robots,NUMERICAL_KEYPAD_MAP_INVERTED['A']))
    for letter in code:
        shortest_path += get_shortest_path_to_press(current_config, letter)
        current_config = get_base_config(n_middle_robots,NUMERICAL_KEYPAD_MAP_INVERTED[letter])
    return shortest_path

codes = []

with open("./21/input.txt", "r") as file:
    for line in file:
        line = line.strip()
        codes.append(line)

#print(codes)

total_complexity = 0

for code in codes:
    shortes_path_for_code = get_shortest_path_for_code(code,N_MIDDLE_ROBOTS)
    #print(f"shortest path for code {code}: {shortes_path_for_code}")
    complexity = int(code[:-1]) * shortes_path_for_code
    #print(f"complexity: {complexity}")
    total_complexity += complexity
    
print(f"part 1 solution: {total_complexity}")
