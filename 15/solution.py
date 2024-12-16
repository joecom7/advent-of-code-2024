# day 15

started_map = False
finished_map = False

n_cols = 0
n_rows = 0

board = {}
robot_pos = (-1,-1)
moves = []

def print_board():
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            print(board[(j,i)],end="")
        print()
        
def evolve_map(move,robot_pos):
    dir = move_map[move]
    equivalent_robot_pos = robot_pos
    
    # boxes chains transmit motion
    found_box_chain = False
    while board[add_tuple(equivalent_robot_pos,dir)] == 'O':
        equivalent_robot_pos = add_tuple(equivalent_robot_pos,dir)
        if not found_box_chain:
            found_box_chain = True
    
    if board[add_tuple(equivalent_robot_pos,dir)] == '.':
        # we can move
        board[robot_pos] = '.'
        robot_pos = add_tuple(robot_pos,dir)
        board[robot_pos] = '@'
        if found_box_chain:
            board[add_tuple(equivalent_robot_pos,dir)] = 'O'
            
    return robot_pos

def calculate_score():
    score = 0
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            if board[(j,i)] == 'O':
                score += 100*j + i
    return score           
                
def add_tuple(a,b):
    return (a[0]+b[0],a[1]+b[1])
            

with open('./15/input.txt', 'r') as file:
    for line in file:
        line = line.strip()
        
        if not started_map:
            started_map = True
            n_cols = len(line)
            # print(n_cols)
            
            for i in range(0,n_cols):
                board[(n_rows,i)] = '#'
                
            n_rows += 1
            
        elif not finished_map:
            if line.count("#") == len(line):
                finished_map = True
            
            for i in range(0,len(line)):
                    
                board[(n_rows,i)] = line[i]
                if line[i] == '@':
                    robot_pos = (n_rows,i)
                    
            n_rows += 1
        
        else:
            for char in line:
                moves.append(char)
            
# print(walls)
# print(boxes)
# print(robot_pos)
# print(moves)

move_map = {
    '^' : (-1, 0),
    'v' : ( 1, 0),
    '<' : ( 0,-1),
    '>' : ( 0, 1)
}

# print("initial state:")
# print_board()

for move in moves:
    robot_pos = evolve_map(move,robot_pos)
    # print()
    # print("-------------")
    # print()
    # print(f"move {move}:")
    # print_board()
    
# print_board()

# for i in range(0,10):
#     robot_pos = evolve_map(moves[i],robot_pos)
#     print(f"move {i}:")
#     print_board()

print(f"part 1 solution: {calculate_score()}")