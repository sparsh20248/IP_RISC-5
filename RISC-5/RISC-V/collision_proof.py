from input import list_of_instructions
from register_accurate import Register


all_registers = Register()

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
    def __init__(self, string):
        self.opcode = string[0:7]
        self.rd = string[7:12]
        self.func3 = string[12:15]
        self.rs1 = string[15:20]
        self.imm = string[20:32]
        self.assign()
    
    def assign(self):
        if(self.func3 == "000"):
            if(self.check()):
                self.ADDI()
            else:
                print("WAITING")
        if(self.func3 == "001"):
            if(self.check()):
                self.SLTI()
        if(self.func3 == "010"):
            if(self.check()):
                self.SLTIU()
        if(self.func3 == "011"):
            if(self.check()):
                self.ANDI()
        if(self.func3 == "100"):
            if(self.check()):
                self.ORI()
        if(self.func3 == "101"):
           if(self.check()):
                self.XORI()
    
    def check(self):
        all_free = 1
        if(not all_registers.check(string_to_int(self.rd))):
            all_free = 0
        if(not all_registers.check(string_to_int(self.rs1))):
            all_free = 0
        
        if(all_free == 0):
            return False
        
        all_registers.book(string_to_int(self.rd))
        all_registers.book(string_to_int(self.rs1))   
        return True
    
    def ADDI(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] + string_to_int(self.imm))
        all_registers.make_free(string_to_int(self.rs1))
        all_registers.make_free(string_to_int(self.rd))
    def STLI(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] < string_to_int(self.imm))
    def STLIU(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] <= string_to_int(self.imm))
    def ANDI(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] & string_to_int(self.imm))
    def ORI(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] | string_to_int(self.imm))
    def XORI(self):
        all_registers.update(string_to_int(self.rd), all_registers.registers[string_to_int(self.rs1)] ^ string_to_int(self.imm))

all_registers.print()
cycles = 1
for i in range(cycles):
    for instruction in list_of_instructions:
        opcode = instruction[0:7]
        if(opcode == "0110011"):
            current = Rtype(instruction)
        if(opcode == "0010011"):
            current = Itype(instruction)
    all_registers.print()

