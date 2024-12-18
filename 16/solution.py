import sys

n_cols = 0
n_rows = 0

board = {}
source = (-1,-1)
end = (-1,-1)
starting_dir = (0,1)

sys.setrecursionlimit(10000)

clockwise_map = {
    ( 0, 1) : ( 1, 0),
    ( 1, 0) : ( 0,-1),
    ( 0,-1) : (-1, 0),
    (-1, 0) : ( 0, 1)
}

counter_clockwise_map = {
    ( 0, 1) : (-1, 0),
    (-1, 0) : ( 0,-1),
    ( 0,-1) : ( 1, 0),
    ( 1, 0) : ( 0, 1)
}

def add_tuple(a,b):
    return (a[0] + b[0], a[1] + b[1])

def add_cost(tuple,cost):
    return (tuple[0],tuple[1]+cost,tuple[2])

def find_lowest_path_recursive(pos=source,dir=starting_dir,partial_results={},visited=[]):
    
    if (pos,dir) in visited:
        return False,0,False
    
    if (pos,dir) in partial_results:
        return partial_results[(pos,dir)]
    
    visited.append((pos,dir))
    valid = True
    
    if board[pos] == '#':
        return_value = False,0,True
        
    elif board[pos] == 'E':
        return_value =  True,0,True
    
    else:    
        costs = []
        
        costs.append(add_cost(find_lowest_path_recursive(pos=add_tuple(pos,dir),
                                                dir=dir,
                                                partial_results=partial_results,visited=visited), 1))
        
        costs.append(add_cost(find_lowest_path_recursive(pos=pos,
                                                dir=clockwise_map[dir],
                                                partial_results=partial_results,visited=visited), 1000))
        
        costs.append(add_cost(find_lowest_path_recursive(pos=pos,
                                                dir=counter_clockwise_map[dir],
                                                partial_results=partial_results,visited=visited), 1000))
        
        valid = all([cost[2] for cost in costs])
        
        if all([not cost[0] for cost in costs]):
            return_value = False,0,valid
        
        else:
            return_value = True,min([cost[1] for cost in costs if cost[0]]),True
            
    visited.pop()
    if return_value[2]:
        partial_results[(pos,dir)] = return_value
    return return_value

def print_board():
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            print(board[(j,i)],end="")
        print()

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
            
print(f"part 1 solution: {find_lowest_path_recursive(pos=source,dir=starting_dir)[1]}")
# print_board()