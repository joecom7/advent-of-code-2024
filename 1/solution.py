# part 2

first_list = []
second_list = []
second_list_occurences_dict = {}

with open("./1/input.txt") as file:
    for line in file:
        numbers = [int(string.strip()) for string in line.split()]
        first_list.append(numbers[0])
        second_list.append(numbers[1])
        if numbers[0] not in second_list_occurences_dict:
            second_list_occurences_dict[numbers[0]] = 0
        if numbers[1] in second_list_occurences_dict:
            second_list_occurences_dict[numbers[1]] += 1
        else:
            second_list_occurences_dict[numbers[1]] = 1
        
first_list.sort()
second_list.sort()

sol_part_1 = 0
sol_part_2 = 0

for (a,b) in zip(first_list,second_list):
    sol_part_1 += abs(a-b)
    sol_part_2 += a*second_list_occurences_dict[a]
    
print(f"part 1 solution: {sol_part_1}")
print(f"part 2 solution: {sol_part_2}")