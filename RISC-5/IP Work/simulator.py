from pipes import Pipes
from basic_functions import *
from input import list_of_instructions
from registers import Register

pc = 0
pipes = Pipes()
all_registers = Register()
PCsrc = False

def instruction_fetch():
    pc = int(pipes.exmem[0])
    pipes.ifid = []
    if PCsrc == True:
        pc+=1
    pipes.ifid.append(pc)
    pipes.ifid.append(list_of_instructions[pc])
    
    # list_of_instructions.pop(pc)
    return

def instruction_decode():
    instruction = pipes.ifid[0]
    opcode = instruction[0:7]
    
    pipes.idex = []
    pipes.idex.append(pc)
    pipes.idex.append(int_to_binary(all_registers[int(instruction[15:20])])) #size?
    pipes.idex.append(int_to_binary(all_registers[int(instruction[15:20])])) #size?
    pipes.idex.append(instruction[:32])
    pipes.idex.append(instruction[12:15])
    pipes.idex.append(instruction[7:12])
    return

def execution():
    instruction = pipes.idex
    # pipes.idex = []
    
    pc = int(instruction[0])
    rs1 = int(instruction[1])
    rs2 = int(instruction[2])
    imm_value = int(instruction[3])
    function = instruction[4]
    
    pipes.exmem = []
    pipes.exmem.append(pc)
    zero = 0
    
    pipes.exam.append(zero)
    if function == "000":
        pipes.exmem.append(rs1 + rs2)
    #more functions will come here?
    
    pipes.exmem.append(instruction[2])
    pipes.exmem.append(instruction[-1])

def memory():
    instruction = pipes.exmem

    pipes.memwb = []
    
    if(instruction[2] == "1"):
        branch()


while(True):
    print("Cycle count: ", pc)
    memory()
    execution()
    instruction_decode()
    instruction_fetch()
    if(pc == len(list_of_instructions) - 1):
        break