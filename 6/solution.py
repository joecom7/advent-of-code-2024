n_rows = 0
n_cols = 0

obstacles = []

officer_pos = (0,0)

explored = 0

with open('./6/input.txt', 'r') as f:
    for line in f:
        
        for i in range(0,len(line)):
            char = line[i]
            if char == '^':
                print(f"found officer at pos {n_cols,i}")
                officer_pos = (n_cols,i)
                explored = 1
                dir = (1,0)
                
            elif char == '#':
                obstacles.append((n_cols,i))
                
        n_rows = len(line)
        n_cols += 1
    
while ((officer_pos[0] >= 0 and officer_pos[0] <= n_cols)) and (
        (officer_pos[1] >= 0 and officer_pos[1] <= n_rows)):
    new_pos = (officer_pos[0] + dir[0],officer_pos[1] + dir[1])
    
    explored += 1
    
    if any(new_pos[0] == obs[0] and new_pos[1] == obs[1] for obs in obstacles):
        if dir == (1,0):
            dir = (0,1)
        elif dir == (0,1):
            dir = (-1,0)
        elif dir == (-1,0):
            dir = (0,-1)
        elif dir == (0,-1):
            dir = (1,0)
    
    officer_pos = new_pos
    
print(f"officer explored {explored} tiles")
