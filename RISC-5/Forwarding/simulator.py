from pipes import Pipes
from basic_functions import *
from input import list_of_instructions
from registers import Register
from wires import Wires

global_pc = 0
pipes = Pipes()
all_registers = Register()
PCsrc = False
wires = Wires()
RAM = dict()
# ALUOp = 0 # 00 for add for load and store 01 for sub and check 0 for beq and any form of func7 or func3 10
# ALUSrc = 0
# MemWrite = False
# MemRead = False
# MemtoReg = False

def ForwardingUnit(exmem_RegWrite, memwb_RegWrite, exmem_Rd, memwb_Rd, read_data1, read_data2):
    control_line1 = 0 
    control_line2 = 0
    if exmem_RegWrite and exmem_Rd!=0 and exmem_Rd == read_data1:
        control_line1 = 2
    if exmem_RegWrite and exmem_Rd!=0 and exmem_Rd == read_data2:
        control_line2 = 2
    if memwb_RegWrite and memwb_Rd!=0 and not (exmem_RegWrite and exmem_Rd!=0 and exmem_Rd == read_data1) and memwb_Rd == read_data1:
        control_line1 = 1
    if memwb_RegWrite and memwb_Rd!=0 and not (exmem_RegWrite and exmem_Rd!=0 and exmem_Rd == read_data2) and memwb_Rd == read_data2:
        control_line2 = 1
    return control_line1, control_line2

def hazard_detection_unit(idex_MemRead, idex_Rd, ifid_ReadRegister1, ifid_ReadRegister2):
    if idex_MemRead and ((idex_Rd == ifid_ReadRegister1) or (idex_Rd == ifid_ReadRegister2)):
        return 1
    return 0

def data_memory(address, data, MemRead, MemWrite):
    print("finally printing to RAM" ,MemRead, MemWrite, address, data)
    if MemWrite:
        RAM[address] = data
        return 0
    if MemRead:
        return RAM[address]
    

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
        print("we are writing in memory", len(pipes.next_idex))
        pipes.next_idex.append(0) #RegWrite
        pipes.next_idex.append(0) #memtoReg
        pipes.next_idex.append(0) #branch taken
        pipes.next_idex.append(0) #memRead
        pipes.next_idex.append(1) #memWrite
        pipes.next_idex.append(0) #ALUOp
        pipes.next_idex.append(1) #ALUSrc
        return

def control_unit(func3, func7, ALUOp):
    print("Control Unit values: ", func3, func7, ALUOp)
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
    if operation == "0000":
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
    opcode = instruction[0:7]
    if opcode == "0100011":
        return string_to_int(instruction[7:12]) + string_to_int(instruction[25:32])*32
    if opcode == "0110111":
        return string_to_int(instruction[20:32])
    return 0

def decode(instruction):
    # opcode = instruction[0:7]
    rd = string_to_int(instruction[7:12])
    func3 = instruction[12:15]
    read_register1 = string_to_int(instruction[15:20]) #5 bit
    read_register2 = string_to_int(instruction[20:25]) #5 bit
    func7 = instruction[25:32]
    return read_register1, read_register2, func3, func7, rd
    

def instruction_fetch(pc):
    if pc >= len(list_of_instructions):
        return pc + 1
    if wires.PCSrc == False:
        global_pc = pc
    next_pc = global_pc + 1
    pipes.next_ifid.append(global_pc)
    pipes.next_ifid.append(list_of_instructions[global_pc])
    return next_pc

def instruction_decode():
    if(pipes.ifid == []):
        return
    pc = pipes.ifid[0]
    instruction = pipes.ifid[1]
    
    control(instruction)

    read_register1, read_register2, func3, func7, rd = decode(instruction)
    ## HAZARD DETECTION UNIT:
    idex_Rd = pipes.idex[-1]
    idex_MemRead = pipes.idex[2]
    stall = hazard_detection_unit(idex_MemRead, idex_Rd, read_register1, read_register2)
    
    #Apply stalling
    
    
    # Hazard detecion unit:
    print("decoded Values: ", instruction, read_register1, read_register2, func3, func7, rd)
    pipes.next_idex.append(pc)
    pipes.next_idex.append(all_registers.get_value(read_register1)) #32 bit
    pipes.next_idex.append(all_registers.get_value(read_register2))  #32 bit
    pipes.next_idex.append(imm_gen(instruction))
    pipes.next_idex.append(func3)
    pipes.next_idex.append(instruction[30])
    pipes.next_idex.append(read_register1)
    pipes.next_idex.append(read_register2)
    pipes.next_idex.append(rd)
    return

def execution():
    if pipes.idex == []:
        return
    RegWrite = pipes.idex[0]
    MemtoReg = pipes.idex[1]
    Branch = pipes.idex[2]
    MemRead = pipes.idex[3]
    MemWrite = pipes.idex[4]
    ALUOp = pipes.idex[5]
    ALUSrc = pipes.idex[6]
    print("Execution control lines: ", RegWrite, MemtoReg, Branch, MemRead, MemWrite, ALUOp, ALUSrc)
    pc = pipes.idex[7]
    read_data1 = pipes.idex[8]
    read_data2 = pipes.idex[9]
    imm_value = pipes.idex[10]
    func3 = pipes.idex[11]
    func7 = pipes.idex[12]
    read_register1 = pipes.idex[13]
    read_register2 = pipes.idex[14]
    rd = pipes.idex[15]
    # print(pipes.idex)
    
    # FORWARDING UNIT
    exmem_RegWrite = pipes.exmem[0]
    memwb_RegWrite = pipes.memwb[0]
    exmem_Rd = pipes.exmem[-1]
    memwb_Rd = pipes.memwb[-1]
    forward1, forward2 = ForwardingUnit(exmem_RegWrite, memwb_RegWrite, exmem_Rd, memwb_Rd, read_register1, read_register2)
    ## Forwarding end
    
    ##ALU Input
    input1 = 0
    input2 = 0
    if forward1 == 0:
        input1 = read_data1
    elif forward1 == 1:
        input1 = wires.result
    elif forward1 == 2:
        input1 = pipes.exmem[7]
    if forward2 == 0:
        input2 = read_data2
    elif forward2 == 1:
        input2 = wires.result
    elif forward2 == 2:
        input2 = pipes.exmem[7]
    
    pc += imm_value
    alu_control_input = control_unit(func3, func7, ALUOp)
    print(input1, input2, alu_control_input)
    if(ALUSrc == 1):
        zero, result = ALU(input1, imm_value, alu_control_input)
    else:
        zero, result = ALU(input1, input2, alu_control_input)
    
    print("Exceution values: ", pc, read_data1, read_data2, imm_value, func3, type(rd), zero, result)
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
    if pipes.exmem == []:
        return
    RegWrite = pipes.exmem[0]
    MemtoReg = pipes.exmem[1]
    Branch = pipes.exmem[2]
    MemRead = pipes.exmem[3]
    MemWrite = pipes.exmem[4] 
    print("Memory control lines: ", RegWrite, MemtoReg, Branch, MemRead, MemWrite)  
    global_pc = pipes.exmem[5]
    zero = pipes.exmem[6]
    address = pipes.exmem[7]
    write_data = pipes.exmem[8]
    rd = pipes.exmem[9]
    print("Memory values: ", global_pc, zero, address, write_data, type(rd))
    
    wires.PCSrc = Branch and zero
    
    read_data = data_memory(address, write_data, MemRead, MemWrite)
    
    pipes.next_memwb.append(RegWrite)
    pipes.next_memwb.append(MemtoReg)
    pipes.next_memwb.append(read_data)
    pipes.next_memwb.append(address)
    pipes.next_memwb.append(rd)
    
def write_back():
    if pipes.memwb == []:
        return
    RegWrite = pipes.memwb[0]
    MemtoReg = pipes.memwb[1]
    read_data = pipes.memwb[2]
    alu_result = pipes.memwb[3]
    rd = pipes.memwb[4]
    print("Write values: ", RegWrite, MemtoReg, read_data, alu_result, type(rd))
    if(RegWrite == 1 and MemtoReg == 1):
        wires.value = read_data
        all_registers.write_back(rd, read_data)
    elif RegWrite == 1:
        wires.value = alu_result
        all_registers.write_back(rd, alu_result)
    return
 
counter = 0
print(list_of_instructions)
all_registers.write_back(1, 5)
next_pc = 0
while(counter < 15):
    print("Cycle count: ", global_pc)
    counter+=1
    next_pc = instruction_fetch(next_pc)
    instruction_decode()
    execution()
    memory()
    write_back()
    global_pc+=1
    pipes.update()
    all_registers.print()
    # if(global_pc >= len(list_of_instructions) - 1):
    #     break
print("Printing RAM")
print(RAM)