N_ROWS = 71
N_COLS = 71
N_FALLEN = 1024
START = (0,0)
END = (N_ROWS - 1, N_COLS - 1)
DIRS = [(-1,0),(1,0),(0,-1),(0,1)]

board = {}

def print_board(board):
    for j in range(-1,N_ROWS+1):
        for i in range(-1,N_COLS+1):
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
        
def find_shortest_path(start,end,costs={}):
    
    unvisited = set()
    costs = {}
    
    for j in range(-1,N_ROWS+1):
        for i in range(-1,N_COLS+1):
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
                    
    return costs[end]

for j in range(-1,N_ROWS+1):
    for i in range(-1,N_COLS+1):
        if j == -1 or j == N_ROWS or i == -1 or i == N_COLS:
            board[(j,i)] = "#"
        else:
            board[(j,i)] = "."

with open('./18/input.txt', 'r') as file:
    added = 0
    for line in file:
        line = line.strip()
        n_strs = line.split(",")
        pos = (int(n_strs[0]),int(n_strs[1]))
        if added < N_FALLEN:
            board[pos] = '#'
            added += 1
        
print(f"part 1 solution: {find_shortest_path(START,END)}")