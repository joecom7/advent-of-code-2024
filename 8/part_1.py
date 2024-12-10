n_rows = 0
n_cols = 0

def compute_antinodes(pos1, pos2):
    vec = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    antinode_1 = (pos2[0] + vec[0], pos2[1] + vec[1])
    antinode_2 = (pos1[0] - vec[0], pos1[1] - vec[1])
    return [antinode_1,antinode_2]

def add_antinodes_for_antenna(locations,antinodes_locations,n_rows,n_cols):
    if len(locations) == 1:
        return
    
    current_location = locations.pop(0)
    for other_location in locations:
        
        for antinode in compute_antinodes(current_location,other_location):
            if ((antinode[0] >= 0 and antinode[0] < n_cols)) and (
                (antinode[1] >= 0 and antinode[1] < n_rows)):
                antinodes_locations.add(antinode)
        
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