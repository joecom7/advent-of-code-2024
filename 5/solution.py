# day 5

def handle_rule(a,b,rules):
    if a in rules:
        rules[a].append(b)
    else:
        rules[a] = [b]
        
def check_line(numbers,rules):
    
    valid = True
    
    for i in range(0,len(numbers)):
        n = numbers[i]
        numbers_without_n = numbers[0:i]
        
        if n in rules and valid:
            if any([other in rules[n] for other in numbers_without_n]):
                valid = False
                
    return valid

def reorder_by_rules(numbers,rules):
    
    reordered_numbers = []
    
    for j in range(0,len(numbers)):
        
        # we need to found the j-th number
        # it is the number that put in j-th pos satisfies
        # all the constraints
        
        found_valid = False
        index_found = -1
        
        for i in range(0,len(numbers)):
            
            if not found_valid:
                
                n = numbers[i]
                numbers_without_n = numbers[0:i] + numbers[i+1:len(numbers)]

                if n not in rules:
                    found_valid = True
                    index_found = i

                else:
                    if not any([other in rules[n] for other in numbers_without_n]):
                        found_valid = True
                        index_found = i
                    
        n = numbers[index_found]
        numbers_without_n = numbers[0:index_found] + numbers[index_found+1:len(numbers)]
        numbers = numbers_without_n
        reordered_numbers.insert(0,n)
        
    return reordered_numbers
        

rules = {}

reached_data = False

count = 0
part_two_count = 0

with open('./5/input.txt', 'r') as f:
    for line in f:
        if line.strip() == "":
            reached_data = True
            #print(rules)
        elif not reached_data:
            a,b = line.split("|")
            handle_rule(int(a),int(b),rules)
        else:
            numbers = [int(n) for n in line.split(",")]
            if check_line(numbers,rules):
                count += numbers[len(numbers)//2]
            else:
                numbers = reorder_by_rules(numbers,rules)
                if not check_line(numbers,rules):
                    raise BaseException("error: reordering algohoritm does not work")
                part_two_count += numbers[len(numbers)//2]
                
print(f"part 1 solution: {count}")
print(f"part 2 solution: {part_two_count}")