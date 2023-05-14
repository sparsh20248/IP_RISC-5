def bin_to_string(string, base):
    # string = string[::-1]
    num = 0
    for i in range(len(string)):
        num*=base
        num+=int(string[i])
    return num

def int_to_binary(number):
    str = ""
    while(number > 0):
        str = str + str(number%2)
        number = number//2
    return str[::-1]

def string_to_int(string, signed = False):
    if(not signed):
        return bin_to_string(string, 2)
    else:
        if(string[0] == '1'): return -bin_to_string(string[1:], 2)
        else: return bin_to_string(string, 2)
        