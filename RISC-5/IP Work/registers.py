class Register:
    registers = []
    free_register = []
    def __init__(self):
        for i in range(32):
            self.registers.append(0)
            
    
    def get_value(self, index):
        return self.registers[index]
        
    def write_back(self, index, value):
        self.registers[index] = value
    
    def print(self):
        for i in range(32):
            if(self.registers[i] != 0):
                print("R" + str(i) + ": " + str(self.registers[i]))