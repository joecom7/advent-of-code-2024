patterns = set()
designs = []


def check_design_possible(design: list[str], patterns: set[str]) -> bool:
    if len(design) == 0:
        return True
    for i in range(1, len(design) + 1):
        if design[:i] in patterns:
            if check_design_possible(design[i:], patterns):
                return True
    return False


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

for design in designs:
    if check_design_possible(design,patterns):
        possible_designs += 1
        
print(f"part 1 solution: {possible_designs}")