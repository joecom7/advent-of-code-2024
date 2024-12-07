import re

# Regular expression with capture groups
pattern = r"mul\((\d+),(\d{1,3})\)"

result = 0

# reading the file
with open('./3/input.txt', 'r') as file:
    data = file.read().replace('\n', '')
    
    # Find all matches in the string
    matches = re.findall(pattern, data)

    # Iterate over the matches (tuples of numbers)
    for match in matches:
        # Each match is a tuple (number1, number2)
        num1, num2 = match
        result += int(num1)*int(num2)
        
print(f"part 1 solution: {result}")

# part 2

# Regular expression with capture groups
pattern = r"mul\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\)"

result = 0
enabled = True

# reading the file
with open('./3/input.txt', 'r') as file:
    data = file.read().replace('\n', '')
    
    # Find all matches in the string
    matches = re.findall(pattern, data)

    # Iterate over the matches (tuples of numbers)
    for match in matches:
        
        num1, num2, do, dont = match
        
        if num1 and num2:
            if enabled:
                result += int(num1)*int(num2)
            
        elif dont:
            enabled = False
        else:
            enabled = True
        
print(f"part 2 solution: {result}")