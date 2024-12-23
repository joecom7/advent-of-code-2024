import re

pattern = r"Button\ A:\ X\+(\d+),\ Y\+(\d+)(\r\n|\r|\n)Button\ B:\ X\+(\d+),\ Y\+(\d+)(\r\n|\r|\n)Prize:\ X=(\d+),\ Y=(\d+)"


def search_min_cost(a_value, b_value, prize_pos):

    det = a_value[0] * b_value[1] - b_value[0] * a_value[1]
    xval = round((1 / det) * (prize_pos[0] * b_value[1] - b_value[0] * prize_pos[1]))
    yval = round((1 / det) * (a_value[0] * prize_pos[1] - prize_pos[0] * a_value[1]))
    if (
        xval * a_value[0] + yval * b_value[0] == prize_pos[0]
        and xval * a_value[1] + yval * b_value[1] == prize_pos[1]
    ):
        return True, 3 * xval + yval
    else:
        return False, 0


total_price = 0

with open("./13/input.txt", "r") as file:
    data = file.read()

    # Find all matches in the string
    matches = re.findall(pattern, data)

    for match in matches:

        found, cost = search_min_cost(
            (int(match[0]), int(match[1])),
            (int(match[3]), int(match[4])),
            (int(match[6]), int(match[7])),
        )
        if found:
            total_price += cost

print(f"part 1 solution: {total_price}")

total_price = 0

with open("./13/input.txt", "r") as file:
    data = file.read()

    # Find all matches in the string
    matches = re.findall(pattern, data)

    for match in matches:

        found, cost = search_min_cost(
            (int(match[0]), int(match[1])),
            (int(match[3]), int(match[4])),
            (10000000000000 + int(match[6]), 10000000000000 + int(match[7])),
        )
        if found:
            total_price += cost
            # print("found solution!")

print(f"part 2 solution: {total_price}")
