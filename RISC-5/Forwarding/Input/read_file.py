inputFile = open("simple1.c.o.dump", "r")
inputFile = inputFile.read()
list_of_instructions = []
temp = ""
for i in inputFile:
    if i != '\n':
        temp += i
    else:
        list_of_instructions.append(temp)
        temp=""
for i in list_of_instructions:
    print(i)
new_intructions = []

index = 0
start = 0
flag = False
for i in range(len(list_of_instructions)):
    if flag:
        new_intructions.append(list_of_instructions[i])
    if list_of_instructions[i] == "00010350 <main>:":
        flag = True
        index = i

print(flag)  
hex_instructions = [] 
for i in new_intructions:
    # print(i, " ++++++", len(i))
    hex_instructions.append(i[10:18])

def make_binary(instruction):
    string = ""
    for i in instruction:
        num = int(i,16)
        temp_string = ""
        for j in range(4):
            temp_string = temp_string + str(num%2)
            num = num//2
        string = string + temp_string[::-1]
    return string

final_instructions = []
for i in hex_instructions:
    print(i)
    final_instructions.append(make_binary(i))
    
for i in final_instructions:
    print(i)

