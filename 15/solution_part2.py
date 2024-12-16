# day 15

started_map = False
finished_map = False

n_cols = 0
n_rows = 0

board = {}
robot_pos = (-1,-1)
moves = []

def can_move_box_chain(equivalent_robot_pos,dir,board):
    if board[equivalent_robot_pos] == '.':
        return True
    elif board[equivalent_robot_pos] == '#':
        return False
    if dir[0] == 0:
        return can_move_box_chain(add_tuple(equivalent_robot_pos,dir),dir,board)
    else:
        if board[equivalent_robot_pos] == '[':
            can_move = can_move_box_chain(add_tuple(equivalent_robot_pos,dir),dir,board)
            can_move = can_move and can_move_box_chain(add_tuple(
                                                    add_tuple(equivalent_robot_pos,(0,1)),dir),dir,board)
            return can_move
        if board[equivalent_robot_pos] == ']':
            can_move = can_move_box_chain(add_tuple(equivalent_robot_pos,dir),dir,board)
            can_move = can_move and can_move_box_chain(add_tuple(
                                                    add_tuple(equivalent_robot_pos,(0,-1)),dir),dir,board)
            return can_move
        if board[equivalent_robot_pos] == '@':
            can_move = can_move_box_chain(add_tuple(equivalent_robot_pos,dir),dir,board)
            return can_move
    return False

def move_box_chain(equivalent_robot_pos,dir,board):
    can_move = can_move_box_chain(equivalent_robot_pos,dir,board)
    if not can_move:
        return can_move
    if board[equivalent_robot_pos] == '.':
        return
    if dir[0] == 0:
        move_box_chain(add_tuple(equivalent_robot_pos,dir),dir,board)
        board[add_tuple(equivalent_robot_pos,dir)] = board[equivalent_robot_pos]
        board[equivalent_robot_pos] = '.'
    else:
        if board[equivalent_robot_pos] == '[':
            move_box_chain(add_tuple(equivalent_robot_pos,dir),dir,board)
            move_box_chain(add_tuple(add_tuple(equivalent_robot_pos,(0,1)),dir),dir,board)
            board[add_tuple(equivalent_robot_pos,dir)] = '['
            board[add_tuple(add_tuple(equivalent_robot_pos,(0,1)),dir)] = ']'
            board[equivalent_robot_pos] = '.'
            board[add_tuple(equivalent_robot_pos,(0,1))] = '.'
        if board[equivalent_robot_pos] == ']':
            move_box_chain(add_tuple(equivalent_robot_pos,dir),dir,board)
            move_box_chain(add_tuple(add_tuple(equivalent_robot_pos,(0,-1)),dir),dir,board)
            board[add_tuple(equivalent_robot_pos,dir)] = ']'
            board[add_tuple(add_tuple(equivalent_robot_pos,(0,-1)),dir)] = '['
            board[equivalent_robot_pos] = '.'
            board[add_tuple(equivalent_robot_pos,(0,-1))] = '.'
        if board[equivalent_robot_pos] == '@':
            move_box_chain(add_tuple(equivalent_robot_pos,dir),dir,board)
            board[add_tuple(equivalent_robot_pos,dir)] = '@'
            board[equivalent_robot_pos] = '.'
    return can_move

def print_board():
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            print(board[(j,i)],end="")
        print()
        
def evolve_map(move,robot_pos):
    dir = move_map[move]
    equivalent_robot_pos = robot_pos
    
    # boxes chains transmit motion
    can_move = move_box_chain(equivalent_robot_pos,dir,board)
            
    if can_move:
        board[robot_pos] = '.'
        robot_pos = add_tuple(robot_pos,dir)
        board[robot_pos] = '@'
            
    return robot_pos

def calculate_score():
    score = 0
    for j in range(0,n_rows):
        for i in range(0,n_cols):
            if board[(j,i)] == '[':
                score += 100*j + i
    return score           
                
def add_tuple(a,b):
    return (a[0]+b[0],a[1]+b[1])
            

with open('./15/input.txt', 'r') as file:
    for line in file:
        line = line.strip()
        
        if not started_map:
            started_map = True
            n_cols = 2*len(line)
            # print(n_cols)
            
            for i in range(0,n_cols):
                board[(n_rows,2*i)] = '#'
                board[(n_rows,2*i+1)] = '#'
                
            n_rows += 1
            
        elif not finished_map:
            if line.count("#") == len(line):
                finished_map = True
            
            for i in range(0,len(line)):
                    
                if line[i] == '@':
                    robot_pos = (n_rows,2*i)
                    board[(n_rows,2*i)] = '@'
                    board[(n_rows,2*i+1)] = '.'
                elif line[i] == 'O':
                    board[(n_rows,2*i)] = '['
                    board[(n_rows,2*i+1)] = ']'
                elif line[i] == '#':
                    board[(n_rows,2*i)] = '#'
                    board[(n_rows,2*i+1)] = '#'
                elif line[i] == '.':
                    board[(n_rows,2*i)] = '.'
                    board[(n_rows,2*i+1)] = '.'
                    
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

print(f"part 2 solution: {calculate_score()}")