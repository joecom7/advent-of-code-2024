# day 2

# reading input

filename = "2/input.txt"

reports = []

def test_report(report):
    sign = report[1] - report[0]
    valid_report = True
    for (a,b) in zip(report[:-1],report[1:]):
        if not((b-a)*sign > 0 and abs(b-a) <= 3):
            valid_report = False
    return valid_report

with open(filename) as file:
    lines = [line.rstrip() for line in file]
    for line in lines:
        report = [int(ele) for ele in line.split()]
        reports.append(report)
        
# part 1

valid_report_count = 0
        
for report in reports:
    valid_report = test_report(report)
    
    if valid_report:
        valid_report_count += 1
        
        
print(f"part 1 solution: {valid_report_count}")

# part 2

valid_report_count = 0
        
for report in reports:
    sign = report[1] - report[0]
    valid_report = test_report(report)
    
    if not valid_report:
        
        # trying all combinations
        
        for i in range(0,len(report)):
            new_list = report[:i] + report[i+1:]
            valid_report = test_report(new_list) or valid_report
    
    if valid_report:
        valid_report_count += 1
        
print(f"part 2 solution: {valid_report_count}")