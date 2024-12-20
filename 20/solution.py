
DIRS = [(-1,0),(1,0),(0,-1),(0,1)]

def print_board(board):
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            print(board[(j,i)],end="")
        print()
        
def find_minimum_cost_node(unvisited,costs):
    minimum_cost = float('inf')
    current_best = None
    for node in unvisited:
        if costs[node] <= minimum_cost:
            minimum_cost = costs[node]
            current_best = node
    return current_best,minimum_cost

def add_tuple(a,b):
    return (a[0] + b[0], a[1] + b[1])

def get_step(pos,dir):
    return add_tuple(pos,dir)

def get_reachable(pos):
    return [get_step(pos,dir) for dir in DIRS]

def get_reachable_by_cheats(pos):
    reachable = []
    for i in DIRS:
        v1 = get_step(pos,i)
        for j in DIRS:
            v2 = get_step(v1,j)
            reachable.append(v2)
    return reachable
                
def get_dist(pos1,pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])
        
def find_shortest_path(start,end,n_rows,n_cols,costs={}):
    
    unvisited = set()
    costs = {}
    
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            if board[(j,i)] != '#':
                unvisited.add((j,i))
                if (j,i) == start:
                    costs[(j,i)] = 0
                else:
                    costs[(j,i)] = float('inf')
                    
    while len(unvisited) != 0:
        node_pos, smallest_distance = find_minimum_cost_node(unvisited,costs)
        unvisited.remove(node_pos)
        
        if smallest_distance == float('inf'):
            break
        
        if node_pos == end:
            break
                
        for new_pos in get_reachable(node_pos):
            if new_pos in unvisited:
                if costs[new_pos] > smallest_distance + 1:
                    costs[new_pos] = smallest_distance + 1
                    
    #print(costs)                
    
    return costs

def find_cheats_saving_times(costs_to,costs_from,source):
    cheats_map = {}
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            pos = (j,i)
            if pos in costs_to:
                for reachable in get_reachable_by_cheats(pos):
                    if reachable in costs_from:
                        new_cost = costs_to[pos] + get_dist(reachable,pos) + costs_from[reachable]
                        if new_cost < costs_from[source]:
                            saving = costs_from[source] - new_cost
                            cheat = (pos,reachable)
                            #print(cheat)
                            if saving not in cheats_map:
                                cheats_map[saving] = set()
                                cheats_map[saving].add(cheat)
                            else:
                                cheats_map[saving].add(cheat)
                            #print(f"cheat {(pos,reachable)} saves {costs_from[source] - new_cost}")
    #print(cheats_map[64])
    return cheats_map

n_cols = 0
n_rows = 0

board = {}
source = (-1,-1)
end = (-1,-1)

with open('./20/input.txt', 'r') as file:
    for line in file:
        line = line.strip()
        
        for i in range(0,len(line)):
            board[(n_rows,i)] = line[i]
            if line[i] == 'S':
                source = (n_rows,i)
            if line[i] == 'E':
                end = (n_rows,i)
                
        n_rows += 1
        if n_rows == 1:     
            n_cols = len(line)
     
costs_to = find_shortest_path(source,end,n_rows,n_cols)   
costs_from = find_shortest_path(end,source,n_rows,n_cols)       
#print(costs_from[source])
cheats_map= find_cheats_saving_times(costs_to,costs_from,source)
threshold = 100
cheat_count = 0
for saving in cheats_map:
    if saving >= threshold:
        cheat_count += len(cheats_map[saving])
        
print(f"part 1 solution: {cheat_count}")