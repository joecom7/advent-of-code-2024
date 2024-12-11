# part 1

def evolve(stone):
    stone_str = str(stone)
    if stone == 0:
        stone_list = [1]
    elif len(stone_str) % 2 == 0:
        stone_list = [int(stone_str[:len(stone_str) // 2]),
                       int(stone_str[(len(stone_str) // 2):])]
    else:
        stone_list = [stone * 2024]
    return stone_list
        
def compute_how_many_stones_recursive(stone:int,n_steps:int,depth:int=0,partial_results={}):
    if (stone,depth) in partial_results:
        ret = partial_results[(stone,depth)]
    else:
        if depth == n_steps:
            ret = 1
        else:
            ret = 0
            for new_stone in evolve(stone):
                ret += compute_how_many_stones_recursive(new_stone,n_steps,depth+1,partial_results)
        partial_results[(stone,depth)] = ret
    return ret

stone_list = []
sim_steps = 75

with open('./11/input.txt', 'r') as f:
    file_content = f.read()
    stone_list = [int(n) for n in file_content.split()]

sol = 0
for stone in stone_list:
    sol += compute_how_many_stones_recursive(stone,sim_steps)
    
print(f"part 1 solution: {sol}")