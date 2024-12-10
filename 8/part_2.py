n_rows = 0
n_cols = 0

def add_tuple(pos, vec):
    return (pos[0] + vec[0], pos[1] + vec[1])

def sub_tuple(pos2,pos1):
    return (pos2[0] - pos1[0], pos2[1] - pos1[1])

def check_in_map(pos, n_rows, n_cols):
    return ((pos[0] >= 0 and pos[0] < n_cols)) and (
                (pos[1] >= 0 and pos[1] < n_rows))

def add_antinodes_for_antenna(locations,antinodes_locations,n_rows,n_cols):
    if len(locations) == 1:
        return
    
    current_location = locations.pop(0)
    for other_location in locations:
        
        vec = sub_tuple(other_location, current_location)
        
        backward_pos = current_location
        
        while check_in_map(backward_pos,n_rows,n_cols):
            antinodes_locations.add(backward_pos)
            backward_pos = sub_tuple(backward_pos,vec)
            
        forward_pos = other_location
        
        while check_in_map(forward_pos,n_rows,n_cols):
            antinodes_locations.add(forward_pos)
            forward_pos = add_tuple(forward_pos,vec)
        
    add_antinodes_for_antenna(locations,antinodes_locations,n_rows,n_cols)
    
antennas_locations = {}
antinodes_locations = set()

with open('./8/input.txt', 'r') as f:
    for line in f:
        
        line = line.strip("\n")
        
        for i in range(0,len(line)):
            if line[i] != '.':
                antenna = line[i]
                if antenna not in antennas_locations:
                    antennas_locations[antenna] = [(n_cols,i)]
                else:
                    antennas_locations[antenna].append((n_cols,i))
                    
                
        n_rows = len(line)
        n_cols += 1
        
for antenna in antennas_locations:
    locations = antennas_locations[antenna]
    add_antinodes_for_antenna(locations,antinodes_locations,n_rows,n_cols)
    
print(len(antinodes_locations))