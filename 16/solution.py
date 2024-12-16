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
    return (a[0]+b[0],a[1]+b[1])

def find_lowest_path_recursive(pos=source,dir=starting_dir,partial_results={}):
    
    if (pos,dir) in partial_results:
        return partial_results[(pos,dir)]
    
    partial_results[(pos,dir)] = -1
    
    if board[pos] == '#':
        return_value = -1
    elif board[pos] == 'E':
        return_value =  0
    else:
        
        path_lengths = [-1,-1,1]
        invalid_paths = [False,False,False]
        
        # try different moves and determine the best
        path_lengths[0] = find_lowest_path_recursive(pos=add_tuple(pos,dir),
                                                dir=dir,
                                                partial_results=partial_results) + 1
        
        if path_lengths[0] == 0:
            invalid_paths[0] = True
        
        path_lengths[1]   = find_lowest_path_recursive(pos=pos,
                                                dir=clockwise_map[dir],
                                                partial_results=partial_results) + 1000
        
        if path_lengths[1] == 999:
            invalid_paths[1] = True
        
        path_lengths[2]  = find_lowest_path_recursive(pos=pos,
                                                dir=counter_clockwise_map[dir],
                                                partial_results=partial_results) + 1000
        
        if path_lengths[2] == 999:
            invalid_paths[2] = True

        if all(invalid_paths):
            return_value = -1
        
        else:
            return_value = min([path_lengths[i] for i in range(0,3) if not invalid_paths[i]])
            
    
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
            
print(f"part 1 solution: {find_lowest_path_recursive(pos=source)}")
# print_board()