# day 12

def check_in_map(pos, n_rows, n_cols):
    return ((pos[0] >= 0 and pos[0] < n_cols)) and (
                (pos[1] >= 0 and pos[1] < n_rows))

def explore_region(j,i,matrix,n_rows,n_cols,visited,letter):
    if (j,i) in visited[letter]:
        return 0,0
    if not check_in_map((j,i),n_rows,n_cols):
        return 0,0
    if not matrix[j][i] == letter:
        return 0,0
    
    visited[letter].add((j,i))
    perimeter = 0
    area = 1
    for j_add in (-1,1):
        added_per,added_area = explore_region(j+j_add,i,matrix,n_rows,n_cols,visited,letter)
        perimeter += added_per
        area += added_area
        if added_area == 0 and (j+j_add,i) not in visited[letter]:
            perimeter += 1
    for i_add in (-1,1):
        added_per,added_area = explore_region(j,i+i_add,matrix,n_rows,n_cols,visited,letter)
        perimeter += added_per
        area += added_area
        if added_area == 0 and (j,i+i_add) not in visited[letter]:
            perimeter += 1
    return perimeter,area

n_rows = 0
n_cols = 0

matrix = []
visited = {}

with open('./12/input.txt', 'r') as f:
    for line in f:
        
        line = line.strip("\n")
        
        new_row = []
        
        for i in range(0,len(line)):
            new_row.append(line[i])
            if line[i] not in visited:
                visited[line[i]] = set()
        matrix.append(new_row)
                
        n_rows = len(line)
        n_cols += 1
    
# print(matrix)

total_price = 0

for j in range(0,n_rows):
    for i in range(0,n_cols):
        letter = matrix[j][i]
        perimeter,area = explore_region(j,i,matrix,n_rows,n_cols,visited,letter)
        if area != 0:
            # print(f"found {letter} region with perimeter {perimeter} and area {area}")
            total_price += area*perimeter
            
print(f"part 1 solution: {total_price}")