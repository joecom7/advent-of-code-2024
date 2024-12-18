
STARTING_DIR = (0,1)

CW_MAP = {
    ( 0, 1) : ( 1, 0),
    ( 1, 0) : ( 0,-1),
    ( 0,-1) : (-1, 0),
    (-1, 0) : ( 0, 1)
}

CCW_MAP = {
    ( 0, 1) : (-1, 0),
    (-1, 0) : ( 0,-1),
    ( 0,-1) : ( 1, 0),
    ( 1, 0) : ( 0, 1)
}

DIRS = [(-1,0),(1,0),(0,-1),(0,1)]

def print_board(board):
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            print(board[(j,i)],end="")
        print()

def add_tuple(a,b):
    return (a[0] + b[0], a[1] + b[1])

def find_minimum_cost_node(unvisited,costs):
    minimum_cost = float('inf')
    current_best = None
    for node in unvisited:
        if costs[node] <= minimum_cost:
            minimum_cost = costs[node]
            current_best = node
    return current_best,minimum_cost

def get_step(pos,dir):
    return add_tuple(pos,dir),dir
    
def get_cw(pos,dir):
    return pos,CW_MAP[dir]

def get_ccw(pos,dir):
    return pos,CCW_MAP[dir]

def get_reachable(pos,dir,cost):
    return [(get_step(pos,dir),cost + 1),
            (get_cw(pos,dir),cost + 1000),
            (get_ccw(pos,dir),cost + 1000)]
    
def get_reaching(pos,dir,cost):
    return [((add_tuple(pos,(-dir[0],-dir[1])),dir),cost - 1),
            (get_cw(pos,dir),cost - 1000),
            (get_ccw(pos,dir),cost - 1000)]

def find_shortest_path(start,end,starting_dir=STARTING_DIR,costs={}):
    
    unvisited = set()
    costs = {}
    
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            for dir in DIRS:
                if board[(j,i)] != '#':
                    unvisited.add(((j,i),dir))
                    if ((j,i),dir) == (start,starting_dir):
                        costs[((j,i),dir)] = 0
                    else:
                        costs[((j,i),dir)] = float('inf')
                    
    while len(unvisited) != 0:
        smallest_distance_node, smallest_distance = find_minimum_cost_node(unvisited,costs)
        unvisited.remove(smallest_distance_node)
        
        if smallest_distance == float('inf'):
            break
        
        node_pos,node_dir = smallest_distance_node
                
        for new_pos,new_cost in get_reachable(node_pos,node_dir,smallest_distance):
            if new_pos in unvisited:
                if costs[new_pos] > new_cost:
                    costs[new_pos] = new_cost
            
    num_nodes_in_best_paths = find_nodes_of_best_paths(start,end,starting_dir,costs)
                    
    return min(costs[(end,dir)] for dir in DIRS),num_nodes_in_best_paths

def find_nodes_of_best_paths(start,end,starting_dir,costs):
    min_cost = min(costs[(end,dir)] for dir in DIRS)
    best_ends = []
    visited = set()
    for pos in costs:
        if costs[pos] == min_cost and pos[0] == end:
            best_ends.append(pos)
            visited.add(pos[0])
    #visited = set(best_ends)
    #print(visited)
    for config in best_ends:
        find_nodes_of_best_paths_recursive(config,costs,visited)
    return len(visited)

def find_nodes_of_best_paths_recursive(config,costs,visited):
    pos = config[0]
    dir = config[1]
    cost = costs[(pos,dir)]
    for reaching_config,reaching_cost in get_reaching(pos,dir,cost):
        reaching_pos, reaching_dir = reaching_config
        if reaching_config in costs and costs[reaching_config] == reaching_cost:
                visited.add(reaching_pos)
                find_nodes_of_best_paths_recursive(reaching_config,costs,visited)
        #print(reaching_pos,reaching_dir,reaching_cost)
        
n_cols = 0
n_rows = 0

board = {}
source = (-1,-1)
end = (-1,-1)

with open('./16/input.txt', 'r') as file:
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
            
result = find_shortest_path(source,end,starting_dir=STARTING_DIR)
print(f"part 1 solution: {result[0]}")
print(f"part 2 solution: {result[1]}")