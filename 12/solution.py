# day 12

def check_in_map(pos, n_rows, n_cols):
    return ((pos[0] >= 0 and pos[0] < n_cols)) and (
                (pos[1] >= 0 and pos[1] < n_rows))

def explore_region(j,i,matrix,n_rows,n_cols,visited,letter,sides):
    if (j,i) in visited[letter]:
        return 0
    if not check_in_map((j,i),n_rows,n_cols):
        return 0
    if not matrix[j][i] == letter:
        return 0
    
    visited[letter].add((j,i))
    area = 1
    for j_add in (-1,1):
        added_area = explore_region(j+j_add,i,matrix,n_rows,n_cols,visited,letter,sides)
        area += added_area
        if added_area == 0 and (j+j_add,i) not in visited[letter]:
            if j_add == -1:
                sides.add(((j,i),(j,i+1),True))
            else:
                sides.add(((j+1,i),(j+1,i+1),False))
    for i_add in (-1,1):
        added_area = explore_region(j,i+i_add,matrix,n_rows,n_cols,visited,letter,sides)
        area += added_area
        if added_area == 0 and (j,i+i_add) not in visited[letter]:
            if i_add == -1:
                sides.add(((j,i),(j+1,i),True))
            else:
                sides.add(((j,i+1),(j+1,i+1),False))
    return area

def collapse_sides_list(sides):
    set_clone = list(sides)
    # print(f"sides before reduction ({len(sides)}): ")
    # for side in sides:
    #     print(side)
    for side in set_clone:
        if side in sides:
            collapse_sides_list_recursive_left(sides,side)
            collapse_sides_list_recursive_right(sides,side)
    # print(f"sides after reduction ({len(sides)}): ")
    # for side in sides:
    #     print(side)
        
def collapse_sides_list_recursive_left(sides,side):
    prev_side = ((2*side[0][0]-side[1][0] , 2*side[0][1]-side[1][1]),side[0],side[2])
    if prev_side in sides:
        collapse_sides_list_recursive_left(sides,prev_side)
        sides.remove(prev_side)
    
def collapse_sides_list_recursive_right(sides,side):
    next_side = (side[1],(2*side[1][0]-side[0][0] , 2*side[1][1]-side[0][1]),side[2])
    if next_side in sides:
        collapse_sides_list_recursive_right(sides,next_side)
        sides.remove(next_side)

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
total_price_part_2 = 0

for j in range(0,n_rows):
    for i in range(0,n_cols):
        letter = matrix[j][i]
        sides = set()
        area = explore_region(j,i,matrix,n_rows,n_cols,visited,letter,sides)
        if area != 0:
            total_price += area*len(sides)
            # print(f"region {letter}")
            collapse_sides_list(sides)
            total_price_part_2 += area*len(sides)
            
print(f"part 1 solution: {total_price}")
print(f"part 2 solution: {total_price_part_2}")