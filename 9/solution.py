# day 9

class block:
    __is_free = False
    __file_id = 0
    
    def __init__(self,is_free,file_id):
        self.__is_free = is_free
        self.__file_id = file_id
        
    def is_free(self):
        return self.__is_free
    
    def get_file_id(self):
        return self.__file_id
    
class block_chain:
    __blocks : list[block] = []
    __files : {int} = set()
    
    def add_block(self,block : block) -> None:
        self.__blocks.append(block)
        if not block.is_free():
            self.__files.add(block.get_file_id())
        
    def print_memory(self) -> None:
        for block in self.__blocks:
            if block.is_free():
                print(".",end="")
            else:
                print(block.get_file_id(),end="")
        print()
                
    def get_first_free_block_address(self,required_len:int=1) -> int :
        for i in range(0,len(self.__blocks)):
            if self.__blocks[i].is_free():
                if len(self.__blocks)-i >= required_len and all([block_i.is_free() for block_i in [self.__blocks[i+j] for j in range(0,required_len)]]):
                    return i
        return -1
    
    def find_file(self, id:int) -> int:
        for i in range(0,len(self.__blocks)):
            if (not self.__blocks[i].is_free()) and self.__blocks[i].get_file_id() == id:
                j = i
                while j< len(self.__blocks) and (not self.__blocks[j].is_free()) and self.__blocks[j].get_file_id() == id:
                    j += 1
                return i,j-i
                
        return -1
            
    def get_last_file_block_address(self) -> int:
        for i in range(len(self.__blocks)-1,-1,-1):
            if not self.__blocks[i].is_free():
                return i
        return -1
    
    def compact_one_block(self):
        
        self.swap_blocks(self.get_first_free_block_address(),
                         self.get_last_file_block_address())
        
        
    def swap_blocks(self,__i,__j,len=1):
        for n in range(0,len):
            i_new = __i + n
            j_new = __j + n
            memory_block = self.__blocks[i_new]
            last_block_address = j_new

            self.__blocks[i_new] = (
                self.__blocks[j_new])

            self.__blocks[last_block_address] = memory_block
        
    def compact_memory(self):
        while self.is_compactable():
            self.compact_one_block()
            self.print_memory()
            
    def compact_files(self):
        files = list(self.__files)
        files.sort(reverse=True)
        for file_id in files:
            file_pos,file_length = self.find_file(file_id)
            if self.get_first_free_block_address(required_len=file_length) != -1 and(
                self.get_first_free_block_address(required_len=file_length) < file_pos):
                self.swap_blocks(self.get_first_free_block_address(required_len=file_length),
                                 file_pos,file_length)
            # self.print_memory()
            
    def get_checksum(self):
        checksum = 0
        for i in range(0,len(self.__blocks)):
            if not self.__blocks[i].is_free():
                checksum += i*self.__blocks[i].get_file_id()
        return checksum
        
    def is_compactable(self):
        return self.get_last_file_block_address() > self.get_first_free_block_address()
        
blocks = block_chain()

with open('./9/input.txt', 'r') as f:
    for line in f:
        
        line = line.strip("\n")
        
        is_file = True
        file_id = -1
        
        for number in [int(number) for number in line]:
            if is_file:
                file_id += 1
                
            for i in range(0,number):
                    blocks.add_block(block(not is_file,file_id))
                
            is_file = not is_file
        
# blocks.print_memory()
# blocks.compact_memory()
# print(f"part 1 solution: {blocks.get_checksum()}")
blocks.compact_files()
print(f"part 2 solution: {blocks.get_checksum()}")