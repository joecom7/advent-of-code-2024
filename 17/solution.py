
class Computer:
    __ip = 0
    __A  = 0
    __B  = 0
    __C  = 0
    __program = []
    __already_printed = False
    __output = ""
    
    def __init__(self,A_i,B_i,C_i,program):
        self.__A = A_i
        self.__B = B_i
        self.__C = C_i
        self.__program = program
    
    def print(self):
        print(f"A content: {self.__A}")
        print(f"B content: {self.__B}")
        print(f"C content: {self.__C}")
        print(f"program: {self.__program}")
        
    def execute_program(self):
        while self.__ip >= 0 and self.__ip < len(program):
            opcode = self.__program[self.__ip]
            
            if opcode == 0:
                self.adv()
            elif opcode == 1:
                self.bxl()
            elif opcode == 2:
                self.bst()
            elif opcode == 3:
                self.jnz()
            elif opcode == 4:
                self.bxc()
            elif opcode == 5:
                self.out()
            elif opcode == 6:
                self.bdv()
            elif opcode == 7:
                self.cdv()
            else:
                raise "invalid opcode"
            
            self.__ip += 2
            
    def execute_program_until_different(self,correct_output):
        while self.__ip >= 0 and self.__ip < len(program) and self.__output in correct_output:
            opcode = self.__program[self.__ip]
            
            if opcode == 0:
                self.adv()
            elif opcode == 1:
                self.bxl()
            elif opcode == 2:
                self.bst()
            elif opcode == 3:
                self.jnz()
            elif opcode == 4:
                self.bxc()
            elif opcode == 5:
                self.out()
            elif opcode == 6:
                self.bdv()
            elif opcode == 7:
                self.cdv()
            else:
                raise "invalid opcode"
            
            self.__ip += 2
        
    def get_combo(self,val):
        if val >= 0 and val <= 3:
            return val
        if val == 4:
            return self.__A
        if val == 5:
            return self.__B
        if val == 6:
            return self.__C
        else:
            raise "invalid combo operand"
        
    def find_A_value(self,A_start=0):
        A_current = A_start
        correct_output = ""
        for val in program:
            if len(correct_output) != 0:
                correct_output += ","
            correct_output += str(val)
        while True:
            self.__ip = 0
            self.__A  = A_current
            self.__B  = 0
            self.__C  = 0
            self.__already_printed = False
            self.__output = ""
            
            self.execute_program_until_different(correct_output)
            if self.__output == correct_output:
                break
            
            if(A_current%1000000 == 0):
                print(f"scanned until {A_current}")
            
            A_current += 1
        
        return A_current
        
    def adv(self):
        operand = self.get_combo(program[self.__ip+1])
        den = 2**operand
        self.__A = self.__A // den
        
    def bxl(self):
        operand = program[self.__ip+1]
        self.__B = self.__B ^ operand
        
    def bst(self):
        operand = self.get_combo(program[self.__ip+1])
        self.__B = operand % 8
        
    def jnz(self):
        if self.__A != 0:
            operand = program[self.__ip+1]
            self.__ip = operand - 2
        
    def bxc(self):
        self.__B = self.__B ^ self.__C
        
    def out(self):
        if self.__already_printed:
            self.__output += ","
        else:
            self.__already_printed = True
        
        operand = self.get_combo(program[self.__ip+1])
        operand = operand % 8
        self.__output += str(operand)
        
    def bdv(self):
        operand = self.get_combo(program[self.__ip+1])
        den = 2**operand
        self.__B = self.__A // den
        
    def cdv(self):
        operand = self.get_combo(program[self.__ip+1])
        den = 2**operand
        self.__C = self.__A // den
        
    def print_output(self):
        print(self.__output)

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

computer = Computer(A_i,B_i,C_i,program)

computer.execute_program()
print("part 1 solution: ",end="")
computer.print_output()

print(f"part 2 solution: {computer.find_A_value()}")


