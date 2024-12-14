import re

pattern = r"p\=(-?\d+),(-?\d+)\ v\=(-?\d+),(-?\d+)"

n_rows = 101
n_cols = 103
n_robots_quads = [0,0,0,0]
n_steps = 100
map = {}
tree_base_length = 8

def check_possible_tree(map) :
    for i in range(0,n_rows):
        for j in range(0,n_cols-tree_base_length):
            if map[(j,i)] != 0:
                if all([map[(j+n,i)] != 0 for n in range(0,tree_base_length)]):
                    return True
    return False

def print_board():
    for j in range(0,n_cols):
        for i in range(0,n_rows):
            count = map[(j,i)]
            if count == 0:
                print(".",end="")
            else:
                print(f"{count}",end="")
        print()

class Robot:
    pos: tuple[int,int]
    vel: tuple[int,int]
    current_quad: int
    initialized_quad:bool = False
    def __init__(self,pos: tuple[int,int],vel: tuple[int,int]):
        self.pos = pos
        self.vel = vel
        map[(self.pos[1],self.pos[0])] += 1
        self.update_quad()
        
    def update_quad(self):
        if self.initialized_quad and self.current_quad != -1:
            n_robots_quads[self.current_quad] -= 1
        self.initialized_quad = True
        if self.pos[0] < n_rows//2 and self.pos[1] < n_cols//2:
            n_robots_quads[0] += 1
            self.current_quad = 0
        elif self.pos[0] < n_rows//2 and self.pos[1] > n_cols//2:
            n_robots_quads[1] += 1
            self.current_quad = 1
        elif self.pos[0] > n_rows//2 and self.pos[1] < n_cols//2:
            n_robots_quads[2] += 1
            self.current_quad = 2
        elif self.pos[0] > n_rows//2 and self.pos[1] > n_cols//2:
            n_robots_quads[3] += 1
            self.current_quad = 3
        else:
            self.current_quad = -1
            
    def print(self):
        print(f"current pos: {self.pos}, current vel: {self.vel}")
        
    def sim_step(self):
        new_pos_0 = self.pos[0] + self.vel[0]
        if new_pos_0 >= n_rows:
            new_pos_0 = new_pos_0 % n_rows
        elif new_pos_0 < 0:
            new_pos_0 = new_pos_0 % n_rows
            
        new_pos_1 = self.pos[1] + self.vel[1]
        if new_pos_1 >= n_cols:
            new_pos_1 = new_pos_1 % n_cols
        elif new_pos_1 < 0:
            new_pos_1 = new_pos_1 % n_cols
            
        map[(self.pos[1],self.pos[0])] -= 1
        self.pos = (new_pos_0,new_pos_1)
        map[(self.pos[1],self.pos[0])] += 1
        self.update_quad()
        
robots: list[Robot] = []
for j in range(0,n_cols):
    for i in range(0,n_rows):
        map[(j,i)] = 0

with open('./14/input.txt', 'r') as file:
    data = file.read()
    
    # Find all matches in the string
    matches = re.findall(pattern, data)

    for match in matches:
        
        robots.append(
            Robot(
            (int(match[0]),int(match[1])),
            (int(match[2]),int(match[3]))
                 )
             )
        
#robots[0].print()
for i in range(0,n_steps):
    for robot in robots:
        robot.sim_step()


result = n_robots_quads[0]
for i in range(1,4):
    result *= n_robots_quads[i]
    #print_board()
    
print(f"part 1 solution: {result}")

new_steps = n_steps

while True:
    new_steps += 1
    for robot in robots:
        robot.sim_step()
    if(check_possible_tree(map)):
        print(f"after {new_steps} steps")
        print_board()
        print()
        print()
        print("-----------------------")
        print()
        print()