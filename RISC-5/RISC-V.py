from input import list_of_instructions
from register_accurate import Register
from pipelines import Pipelines 

all_registers = Register()
all_pipes = Pipelines()
pc = 0


def bin_to_string(string, base):
    # string = string[::-1]
    num = 0
    for i in range(len(string)):
        num*=base
        num+=int(string[i])
    return num

def string_to_int(string, signed = False):
    if(not signed):
        return bin_to_string(string, 2)
    else:
        if(string[0] == '1'): return -bin_to_string(string[1:], 2)
        else: return bin_to_string(string, 2)

class Rtype:
    def __init__(self, string):
        self.opcode = string[0:7]
        self.rd = string[7:12]
        self.func3 = string[12:15]
        self.rs1 = string[15:20]
        self.rs2 = string[20:25]
        self.func7 = string[25:32]
        self.assign()
        
    def assign(self):
        
        if(self.func3 == "000"):
            self.ADD()
        if(self.opcode == ""):
            self.SUB()
        if(self.opcode == ""):
            self.SLT()
        if(self.opcode == ""):
            self.SLTU()
        if(self.opcode == ""):
            self.AND()
        if(self.opcode == ""):
            self.OR()
        if(self.opcode == ""):
            self.XOR()
        if(self.opcode == ""):
            self.SRA()
        if(self.opcode == ""):
            self.SLL()
        if(self.opcode == ""):
            self.SRL()
    
    def ADD(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] + all_registers.registers[string_to_int(self.rs2)])
    def SUB(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] - all_registers.registers[string_to_int(self.rs2)])
    def SLT(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] < all_registers.registers[string_to_int(self.rs2)])    
    def SLTU(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] < all_registers.registers[string_to_int(self.rs2)])
    
class Itype:
    def __init__(self, string, pcounter):
        self.opcode = string[0:7]
        self.rd = string[7:12]
        self.func3 = string[12:15]
        self.rs1 = string[15:20]
        self.imm = string[20:32]
        value = 0
    
    def assign(self):
        if(self.func3 == "000"):
            if(self.check()):
                self.ADDI()
                return True
            else:
                print("WAITING")
        if(self.func3 == "001"):
            if(self.check()):
                self.SLTI()
                return True
            else:
                print("WAITING")
        if(self.func3 == "010"):
            if(self.check()):
                self.SLTIU()
                return True
            else:
                print("WAITING")
        if(self.func3 == "011"):
            if(self.check()):
                self.ANDI()
                return True
            else:
                print("WAITING")
        if(self.func3 == "100"):
            if(self.check()):
                self.ORI()
                return True
            else:
                print("WAITING")
        if(self.func3 == "101"):
            if(self.check()):
                self.XORI()
                return True
            else:
                print("WAITING")
        return False
    
    def check(self, book = False):
        all_free = 1
        if(not all_registers.check(string_to_int(self.rd))):
            all_free = 0
        if(not all_registers.check(string_to_int(self.rs1))):
            all_free = 0
        if(all_free == 0):
            return False  
        if(book):
            all_registers.book(string_to_int(self.rd))
            all_registers.book(string_to_int(self.rs1))
        return True
    
    def ADDI(self):
        self.value = all_registers.registers[string_to_int(self.rs1)] + string_to_int(self.imm)
    def STLI(self):
        self.value = all_registers.registers[string_to_int(self.rs1)] < string_to_int(self.imm)
    def STLIU(self):
        self.value = all_registers.registers[string_to_int(self.rs1)] <= string_to_int(self.imm)
    def ANDI(self):
        self.value = all_registers.registers[string_to_int(self.rs1)] & string_to_int(self.imm)
    def ORI(self):
        self.value = all_registers.registers[string_to_int(self.rs1)] | string_to_int(self.imm)
    def XORI(self):
        self.value = all_registers.registers[string_to_int(self.rs1)] ^ string_to_int(self.imm)

    def write_back(self):
        all_registers.update(string_to_int(self.rd), self.value)

#all_registers.print()
def read_stage(instruction):
    if(len(list_of_instructions) == 0): return
    instruction = list_of_instructions[0]
    list_of_instructions.pop(0)
    opcode = instruction[0:7]
    if(opcode == "0110011"): current = Rtype(instruction)
    if(opcode == "0010011"): current = Itype(instruction)
    all_pipes.read_pipe.append(current)

def execute_stage():
    if(len(all_pipes.read_pipe) == 0): return
    current = all_pipes.read_pipe[0]
    if(current.check(book = True)):
        all_pipes.read_pipe.pop(0)
        all_pipes.execute_pipe.append(current)
    return
    
def write_stage():
    if(len(all_pipes.execute_pipe) == 0): return
    current = all_pipes.execute_pipe[0]
    current.assign()
    return

def commit_stage():
    return

while(True):
    pc+=1
    read_stage()
    
    execute_stage()
    
    write_stage()
    
    commit_stage()

    if(all_pipes.check()):
        break
    all_registers.print()


