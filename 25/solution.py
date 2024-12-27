keys = set()
locks = set()
i = 0
in_key = True
in_lock = False


def key_lock_match(key, lock):
    for i in range(0, 5):
        if key[i] + lock[i] > 5:
            return False
    return True


def get_all_matches(key, locks):
    result = 0
    for lock in locks:
        if key_lock_match(key, lock):
            result += 1
    return result


with open("./25/input.txt", "r") as file:
    for line in file:
        line = line[:-1]
        if (i % 8) == 0:
            if i > 0:
                if in_key:
                    keys.add(tuple(found))
                if in_lock:
                    locks.add(tuple(found))
            if line.count(".") == len(line):
                in_key = True
                in_lock = False
                to_find = [True for _ in range(0, 5)]
                found = [0 for _ in range(0, 5)]
            elif line.count("#") == len(line):
                in_key = False
                in_lock = True
                to_find = [True for _ in range(0, 5)]
                found = [0 for _ in range(0, 5)]
            else:
                print(f"error: {line}")

        for j in range(0, 5):
            if to_find[j]:
                if in_key and line[j] == "#":
                    to_find[j] = False
                    found[j] = 8 - i % 8 - 2
                elif in_lock and line[j] == ".":
                    to_find[j] = False
                    found[j] = i % 8 - 1

        i += 1
    if in_key:
        keys.add(tuple(found))
    if in_lock:
        locks.add(tuple(found))

result = 0
for key in keys:
    result += get_all_matches(key, locks)
print(f"part 1 solution: {result}")
