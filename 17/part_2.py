

A_i = 0
B_i = 0
C_i = 0
program = []

with open('./17/input.txt', 'r') as file:
    for line in file:
        if(line.startswith("Register A: ")):
            A_i = int(line[len("Register A: "):])
        elif(line.startswith("Register B: ")):
            B_i = int(line[len("Register B: "):])
        elif(line.startswith("Register C: ")):
            C_i = int(line[len("Register C: "):])
        elif(line.startswith("Program: ")):
            program = [num for num in [int(numstr) for numstr in line[len("Program: "):].split(",")]]
            
B_values = program[::-1]
            
def find_possible_A_sequence_recursive(current_A,B_values,depth=0):
    for new_A in range(0,8):
        computed_new_A = (current_A << 3) + new_A
        B = ((computed_new_A & 7^1)^(computed_new_A>>((computed_new_A & 7^1)))^4) & 7
        if B == B_values[depth]:
            if depth < len(B_values)-1:
                found,correct_A = find_possible_A_sequence_recursive(computed_new_A,B_values,depth=depth+1)
                if found:
                    return True,correct_A
            else:
                return True,computed_new_A
    return False,None
            
print(f"part 2 solution: {find_possible_A_sequence_recursive(0,B_values,depth=0)[1]}")


