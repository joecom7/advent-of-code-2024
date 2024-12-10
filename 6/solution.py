
def is_pos_in_matrix(officer_pos, n_rows, n_cols):
    return ((officer_pos[0] >= 0 and officer_pos[0] < n_cols)) and (
        (officer_pos[1] >= 0 and officer_pos[1] < n_rows))
    
new_dir_map = {
    (-1,0) :  (0,1),
    (0,1)  :  (1,0),
    (1,0)  :  (0,-1),
    (0,-1) :  (-1,0)
}

def compute_new_dir(dir):
    return new_dir_map[dir]

def check_officer_path(officer_start, starting_dir, n_rows, n_cols,obstacles):
    
    visited = {}
    in_loop = False
    dir = starting_dir
    
    officer_pos = officer_start
    
    while is_pos_in_matrix(officer_pos, n_rows, n_cols) and not in_loop:
    
        # where should the officer move based on current direction

        new_pos = (officer_pos[0] + dir[0],officer_pos[1] + dir[1])

        while new_pos in obstacles:

            # there is an obstacle in that direction

            dir = compute_new_dir(dir)
            new_pos = (officer_pos[0] + dir[0],officer_pos[1] + dir[1])

        # still not exited

        if not officer_pos in visited:
            visited[officer_pos] = {dir}

        else:
            if dir in visited[officer_pos]:
                in_loop = True
            visited[officer_pos].add(dir)

        # make the step

        officer_pos = new_pos
    
    return visited,in_loop

n_rows = 0
n_cols = 0

obstacles = set()

with open('./6/input.txt', 'r') as f:
    for line in f:
        
        for i in range(0,len(line)):
            char = line[i]
            if char == '^':
                officer_start = (n_cols,i)
                starting_dir = (-1,0)
                
            elif char == '#':
                obstacles.add((n_cols,i))
                
        n_rows = len(line)
        n_cols += 1
    
visited,in_loop = check_officer_path(officer_start,starting_dir,n_rows,n_cols,obstacles)
    
print(f"part 1 solution: {len(visited)}")
potential_loops = 0

for j in range(0,n_rows):
    for i in range(0,n_cols):
        if not (j == officer_start[0] and i == officer_start[1]):
            obstacles_augmented = obstacles.copy()
            obstacles_augmented.add((j,i))
            if check_officer_path(officer_start,starting_dir,n_rows,n_cols,obstacles_augmented)[1]:
                potential_loops += 1
        
print(f"part 2 solution: {potential_loops}")