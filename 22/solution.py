from typing import Dict


def mix(s, n):
    return s ^ n


def prune(n):
    return n % 16777216


def get_next_secret_number(n: int, cache: Dict[int, int]):
    if n in cache:
        return cache[n]
    n0 = n
    a = n * 64
    n = mix(n, a)
    n = prune(n)
    b = n // 32
    n = mix(n, b)
    n = prune(n)
    c = n * 2048
    n = mix(n, c)
    n = prune(n)
    cache[n0] = n
    return cache[n0]


def get_price(n):
    return n % 10


initial_secret_numbers = []
sequences_map = {}
cache = {}

with open("./22/input.txt", "r") as file:
    i = 0
    for line in file:
        line = line.strip()
        initial_secret_numbers.append(int(line))
        i += 1

result = 0

for n in initial_secret_numbers:

    old_price = get_price(n)
    seen_change_sequences = set()
    change_sequence = []
    change_sequence.append(0)

    for j in range(0, 2000):
        n = get_next_secret_number(n, cache)
        new_price = get_price(n)
        change_sequence.append(new_price-old_price)
        if j>= 3:
            change_sequence.pop(0)
        if j>=2:
            change_sequence_tuple = tuple(change_sequence)
            #print(change_sequence_tuple)
            if not change_sequence_tuple in seen_change_sequences:
                seen_change_sequences.add(change_sequence_tuple)
                if not change_sequence_tuple in sequences_map:
                    sequences_map[change_sequence_tuple] = new_price
                else:
                    sequences_map[change_sequence_tuple] += new_price
        old_price = new_price

    result += n
    
max_bananas = 0
best_sequence = None

for sequence in sequences_map:
    if sequences_map[sequence] > max_bananas:
        max_bananas = sequences_map[sequence]
        best_sequence = sequence
        
print(f"part 2 solution: {sequences_map[best_sequence]}")