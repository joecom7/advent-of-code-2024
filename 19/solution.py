patterns = set()
designs = []


def check_design_possible(
    design: list[str], patterns: set[str], partial_results={}
) -> int:
    if design in partial_results:
        return partial_results[design]
    possible_designs = 0
    if len(design) == 0:
        possible_designs = 1
    else:
        for i in range(1, len(design) + 1):
            if design[:i] in patterns:
                possible_designs += check_design_possible(design[i:], patterns)
    partial_results[design] = possible_designs
    return possible_designs


with open("./19/input.txt", "r") as file:
    added = 0
    found_patterns = False
    for line in file:
        line = line.strip()
        if not len(line) == 0:
            if not found_patterns:
                line = line.replace(" ", "")
                patterns = set(line.split(","))
                found_patterns = True
            else:
                designs.append(line)

possible_designs = 0
n_combinations = 0

for design in designs:
    n_combinations_new = check_design_possible(design, patterns)
    if n_combinations_new > 0:
        possible_designs += 1
        n_combinations += n_combinations_new

print(f"part 1 solution: {possible_designs}")
print(f"part 2 solution: {n_combinations}")
