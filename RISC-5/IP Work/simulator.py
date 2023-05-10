from pipes import Pipes
from basic_functions import *
from input import list_of_instructions
from registers import Register

global_pc = 0
pipes = Pipes()
all_registers = Register()
PCsrc = False
next_pc = 0
# ALUOp = 0 # 00 for add for load and store 01 for sub and check 0 for beq and any form of func7 or func3 10
# ALUSrc = 0
# MemWrite = False
# MemRead = False
# MemtoReg = False

def data_memory(address, data, MemWrite, MemRead):
    return

def control(instruction):
    opcode = instruction[0:7]
    if opcode == "0110111": #load immediate
        pipes.next_idex.append(1) #RegWrite
        pipes.next_idex.append(1) #memtoReg
        pipes.next_idex.append(0) #branch taken
        pipes.next_idex.append(1) #memRead
        pipes.next_idex.append(0) #memWrite
        pipes.next_idex.append(0) #ALUOp
        pipes.next_idex.append(1) #ALUSrc
        return 
    if opcode == "1100011": #branch
        pipes.next_idex.append(0) #RegWrite
        pipes.next_idex.append(0) #memtoReg
        pipes.next_idex.append(1) #branch taken
        pipes.next_idex.append(0) #memRead
        pipes.next_idex.append(0) #memWrite
        pipes.next_idex.append(1) #ALUOp
        pipes.next_idex.append(0) #ALUSrc
        return
    if opcode == "0110011": #add
        pipes.next_idex.append(1) #RegWrite
        pipes.next_idex.append(0) #memtoReg
        pipes.next_idex.append(0) #branch taken
        pipes.next_idex.append(0) #memRead
        pipes.next_idex.append(0) #memWrite
        pipes.next_idex.append(2) #ALUOp
        pipes.next_idex.append(0) #ALUSrc
        return
    if opcode == "0100011": #store
        pipes.next_idex.append(0) #RegWrite
        pipes.next_idex.append(0) #memtoReg
        pipes.next_idex.append(0) #branch taken
        pipes.next_idex.append(0) #memRead
        pipes.next_idex.append(1) #memWrite
        pipes.next_idex.append(0) #ALUOp
        pipes.next_idex.append(1) #ALUSrc
        return

def control_unit(func3, func7, ALUOp):
    if ALUOp == 0: #load and store
        return "0010"
    if ALUOp == 1: #branch
        return "0110"
    if ALUOp == 2:
        if func7 == "0" and func3 == "000":
            return "0010" #add
        if func7 == "1" and func3 == "000":
            return "0110" #substract
        if func7 == "0000000" and func3 == "111":
            return "0000" #and
        if func7 == "0000000" and func3 == "110":
            return "0001" #or
    

def ALU(read_data1, read_data2, operation):
    if operation == "0010":
        #AND
        return 0 , (read_data1 & read_data2)
    if operation == "0001":
        #OR
        return 0 , (read_data1 | read_data2)
    if operation == "0010":
        #ADD
        return 0 , (read_data1 + read_data2)
    if operation == "0110":
        #Substract
        return 0 , (read_data1 - read_data2)


def imm_gen(instruction): 
    return instruction

def decode(instruction):
    opcode = instruction[0:7]
    rd = string_to_int(instruction[7:12])
    func3 = string_to_int(instruction[12:15])
    read_register1 = string_to_int(instruction[15:20]) #5 bit
    read_register2 = string_to_int(instruction[20:25]) #5 bit
    func7 = string_to_int(instruction[25:32])
    return read_register1, read_register2, func3, func7, rd
    

def instruction_fetch():
    
    if PCsrc == False:
        global_pc = next_pc
    next_pc = global_pc + 1
    pipes.next_ifid.append(global_pc)
    pipes.next_ifid.append(list_of_instructions[global_pc])
    return

def instruction_decode():
    pc = pipes.ifid[0]
    instruction = pipes.ifid[1]
    
    control(instruction)

    read_data1, read_data2, func3, func7, rd = decode(instruction)

    pipes.next_idex.append(pc)
    pipes.next_idex.append(all_registers.get_value(read_data1)) #32 bit
    pipes.next_idex.append(all_registers.get_value(read_data2))  #32 bit
    pipes.next_idex.append(imm_gen(instruction))
    pipes.next_idex.append(func3)
    # pipes.next_idex.append(func7)
    pipes.next_idex.append(rd)
    return

def execution():
    RegWrite = pipes.idex[0]
    MemtoReg = pipes.idex[1]
    Branch = pipes.idex[2]
    MemRead = pipes.idex[3]
    MemWrite = pipes.idex[4]
    ALUOp = pipes.idex[5]
    ALUSrc = pipes.idex[6]
    pc = pipes.idex[7]
    read_data1 = pipes.idex[8]
    read_data2 = pipes.idex[9]
    imm_value = pipes.idex[10]
    func3 = pipes.idex[11]
    # func7 = pipes.idex[5]
    rd = pipes.idex[12]
    
    pc += imm_value
    alu_control_input = control_unit(func3, ALUOp)
    if(ALUSrc == 1):
        zero, result = ALU(read_data1, imm_value, alu_control_input)
    else:
        zero, result = ALU(read_data1, read_data2, alu_control_input)
    
    pipes.next_exmem.append(RegWrite)
    pipes.next_exmem.append(MemtoReg)
    pipes.next_exmem.append(Branch)
    pipes.next_exmem.append(MemRead)
    pipes.next_exmem.append(MemWrite)
    pipes.next_exmem.append(pc)
    pipes.next_exmem.append(zero)
    pipes.next_exmem.append(result)
    pipes.next_exmem.append(read_data2)
    pipes.next_exmem.append(rd)
    

def memory():
    RegWrite = pipes.idex[0]
    MemtoReg = pipes.idex[1]
    Branch = pipes.idex[2]
    MemRead = pipes.idex[3]
    MemWrite = pipes.idex[4]   
    global_pc = pipes.idex[5]
    zero = pipes.idex[6]
    address = pipes.idex[7]
    write_data = pipes.idex[8]
    rd = pipes.idex[9]
    
    PCsrc = Branch and zero
    
    read_data = data_memory(address, write_data, MemRead, MemWrite)
    
    pipes.next_memwb.append(RegWrite)
    pipes.next_memwb.append(MemtoReg)
    pipes.next_memwb.append(read_data)
    pipes.next_memwb.append(rd)
    
    
counter = 0
while(counter < 100):
    print("Cycle count: ", global_pc)
    counter+=1
    instruction_fetch()
    instruction_decode()
    execution()
    memory()
    global_pc+=1
    pipes.update()
    if(global_pc >= len(list_of_instructions) - 1):
        break