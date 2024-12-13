import math
import re

pattern = r"Button\ A:\ X\+(\d+),\ Y\+(\d+)(\r\n|\r|\n)Button\ B:\ X\+(\d+),\ Y\+(\d+)(\r\n|\r|\n)Prize:\ X=(\d+),\ Y=(\d+)"

from sympy import symbols, Eq, solve
from sympy.solvers.diophantine import diophantine

def search_min_cost(a_value,b_value,prize_pos):
    
    x, y, t = symbols('x y t')
    eq1 = a_value[0]*x + b_value[0]*y - prize_pos[0]
    eq2 = a_value[1]*x + b_value[1]*y - prize_pos[1]
    try:
        sol = diophantine(eq1, t, syms=[x, y])
        [xt, yt], = sol
        eq3 = eq2.subs({x:xt, y:yt})
        t1, = eq3.free_symbols
        [t1s], = diophantine(eq3, y, syms=[t1])
        rep = {t1:t1s}
        return True,3*xt.subs(rep) + yt.subs(rep)
    except:
        return False,0
    
total_price = 0

with open('./13/input.txt', 'r') as file:
    data = file.read()
    
    # Find all matches in the string
    matches = re.findall(pattern, data)

    for match in matches:
        
        found,cost = search_min_cost(
              (int(match[0]),int(match[1])),
              (int(match[3]),int(match[4])),
              (int(match[6]),int(match[7])))
        if found:
            total_price += cost
            
print(f"part 1 solution: {total_price}")

total_price = 0

with open('./13/input.txt', 'r') as file:
    data = file.read()
    
    # Find all matches in the string
    matches = re.findall(pattern, data)

    for match in matches:
        
        found,cost = search_min_cost(
              (int(match[0]),int(match[1])),
              (int(match[3]),int(match[4])),
              (10000000000000 + int(match[6]),10000000000000 + int(match[7])))
        if found:
            total_price += cost
            # print("found solution!")
            
print(f"part 2 solution: {total_price}")