# day 7

import re

def check_equation_possible_recursive(result,numbers_left,partial_result,operator,enable_concat):
    first_number = numbers_left[0]
    
    if operator == '+':
        new_partial_result = partial_result + first_number
    elif operator == '*':
        new_partial_result = partial_result * first_number
    elif operator == '|':
        new_partial_result = int(str(partial_result) + str(first_number))
    
    if len(numbers_left) == 1:
        if result == new_partial_result:
            return True
        else:
            return False

    if check_equation_possible_recursive(result,numbers_left[1:],new_partial_result,'+',enable_concat):
        return True
    elif check_equation_possible_recursive(result,numbers_left[1:],new_partial_result,'*',enable_concat):
        return True
    elif enable_concat:
        if check_equation_possible_recursive(result,numbers_left[1:],new_partial_result,'|',enable_concat):
            return True
        else:
            return False
    return False
    

def check_equation_possible(result,numbers,enable_concat):
    first_number = numbers[0]
    if len(numbers) == 1:
        if result == first_number:
            return True
        else:
            return False
    if check_equation_possible_recursive(result,numbers[1:],first_number,'+',enable_concat):
        return True
    elif check_equation_possible_recursive(result,numbers[1:],first_number,'*',enable_concat):
        return True
    elif enable_concat:
        if check_equation_possible_recursive(result,numbers[1:],first_number,'|',enable_concat):
            return True
        else:
            return False
    return False

# Regular expression with capture groups
pattern = r"(\d+):\s((\d*(\s)*)+)"

total_value = 0
total_value_with_just_concat = 0

with open('./7/input.txt', 'r') as f:
    for line in f:
        
        # Find all matches in the string
        matches = re.findall(pattern, line)
        result = int(matches[0][0])
        numbers = [int(n) for n in matches[0][1].split()]
        
        if check_equation_possible(result,numbers,False):
            total_value += result
        elif check_equation_possible(result,numbers,True):
            total_value_with_just_concat += result
            
            
print(f"part 1 solution: {total_value}")
print(f"part 2 solution: {total_value + total_value_with_just_concat}")