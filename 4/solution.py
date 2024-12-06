
# day 4

# part 1

def search_recursive(matrix,j,i,obj,height,width) -> int:
    
    num_matches = 0
    
    if matrix[j][i] != obj[0]:
        return 0
    
    for j_add in range(-1,2):
        for i_add in range(-1,2):
            if search_recursive_fixed_dir(matrix,j+j_add,i+i_add,
                                            1,obj,height,width,j_add,i_add):
                num_matches += 1
            
    return num_matches

def search_recursive_fixed_dir(matrix,j,i,depth,obj,height,width,j_add,i_add) -> int:
    
    if j < 0 or j >= height:
        return False
    
    if i < 0 or i >= width:
        return False
    
    if matrix[j][i] != obj[depth]:
        return False
    
    if depth == 3:
        return True
    
    return search_recursive_fixed_dir(matrix,j+j_add,i+i_add,
                                            depth+1,obj,height,width,j_add,i_add)

with open('./4/input.txt', 'r') as f:
    matrix = [[*line] for line in f]
    
obj = "XMAS"
    
height = len(matrix)
width = len(matrix[0]) - 1

num_matches_global = 0

for j in range(0,height):
    for i in range(0,width):
        # print(search_recursive(matrix,j,i,obj,height,width))
        num_matches_global += search_recursive(matrix,j,i,obj,height,width)
        
print(f"part 1 solution: {num_matches_global}")

# part 2

count = 0

for j in range(1,height-1):
    for i in range(1,width-1):
        if matrix[j][i] == 'A':
            if (matrix[j-1][i-1] == 'M' and matrix[j+1][i+1] == 'S') or  (
                matrix[j-1][i-1] == 'S' and matrix[j+1][i+1] == 'M'):
                if (matrix[j-1][i+1] == 'M' and matrix[j+1][i-1] == 'S') or  (
                    matrix[j-1][i+1] == 'S' and matrix[j+1][i-1] == 'M'):
                        count += 1
                        
print(f"part 2 solution: {count}")