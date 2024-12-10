
def check_point_in_matrix(j,i,n_rows,n_cols):
    return (i >= 0) and (i < n_rows) and (j >= 0) and (j < n_cols)
    
def compute_reachable_nines(j, i, matrix, n_rows, n_cols, reachable_nines, visited,depth=0):
    if check_point_in_matrix(j,i,n_rows,n_cols):
        if matrix[j][i] == depth and (j,i) not in visited:
            if depth == 9:
                reachable_nines.add((j,i))
            else:
                visited.add((j,i))
                compute_reachable_nines(j-1, i, matrix, n_rows, n_cols, reachable_nines, visited, depth+1)
                compute_reachable_nines(j+1, i, matrix, n_rows, n_cols, reachable_nines, visited, depth+1)
                compute_reachable_nines(j, i-1, matrix, n_rows, n_cols, reachable_nines, visited, depth+1)
                compute_reachable_nines(j, i+1, matrix, n_rows, n_cols, reachable_nines, visited, depth+1)
                
def compute_different_trailheads(j, i, matrix, n_rows, n_cols, visited,depth=0):
    if check_point_in_matrix(j,i,n_rows,n_cols):
        if matrix[j][i] == depth and (j,i) not in visited:
            if depth == 9:
                return 1
            else:
                visited.append((j,i))
                value = 0
                value += compute_different_trailheads(j-1, i, matrix, n_rows, n_cols, visited, depth+1)
                value += compute_different_trailheads(j+1, i, matrix, n_rows, n_cols, visited, depth+1)
                value += compute_different_trailheads(j, i-1, matrix, n_rows, n_cols, visited, depth+1)
                value += compute_different_trailheads(j, i+1, matrix, n_rows, n_cols, visited, depth+1)
                visited.pop()
                return value
    return 0

n_rows = 0
n_cols = 0

matrix = []

with open('./10/input.txt', 'r') as f:
    for line in f:
        
        line = line.strip("\n")
        
        new_row = []
        
        for i in range(0,len(line)):
            new_row.append(int(line[i]))
        matrix.append(new_row)
                
        n_rows = len(line)
        n_cols += 1
    
totale_score_first_part = 0
totale_score_second_part = 0
    
for j in range(0,n_rows):
    for i in range(0,n_cols):
        reachable_nines = set()
        visited = set()
        visited_2 = []
        compute_reachable_nines(j, i, matrix, n_rows, n_cols, reachable_nines, visited)
        totale_score_first_part += len(reachable_nines)
        totale_score_second_part += compute_different_trailheads(j, i, matrix, n_rows, n_cols, visited_2)
        
print(f"part 1 solution: {totale_score_first_part}")
print(f"part 2 solution: {totale_score_second_part}")