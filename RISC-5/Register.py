class Register:
    registers = []
    def __init__(self):
        for i in range(32):
            self.registers.append(0)
            
    def update(self, index, value):
        print(index, type(index))
        self.registers[index] = value
        
    def print(self):
        for i in range(32):
            print("x" + str(i) + ": " + str(self.registers[i]))