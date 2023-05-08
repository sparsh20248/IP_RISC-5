class Register:
    registers = []
    free_register = []
    def __init__(self):
        for i in range(32):
            self.registers.append(0)
            self.free_register.append(0)
            
    
    def check (self, index):
        return self.free_register[index] == 0
    
    def book (self, index):
        if(self.check(index)):
            self.free_register[index] = 1
            return True
        return False
        
    def update(self, index, value):
        print(index, type(index))
        self.registers[index] = value
    
    def make_free(self, index):
        self.free_register[index] = 0
        
    def print(self):
        for i in range(32):
            print("x" + str(i) + ": " + str(self.registers[i]))