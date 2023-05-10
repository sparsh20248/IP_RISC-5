class Pipes:
    ifid = []
    idex = []
    exmem = []
    memwb = []
    next_ifid = []
    next_idex = []
    next_exmem = []
    next_memwb = []
    persistant_next_ifid = []
    persistant_next_idex = []
    persistant_next_exmem = []
    persistant_next_memwb = []
    
    def update(self):
        self.persistant_next_exmem.append(self.next_exmem)
        self.persistant_next_idex.append(self.next_idex)
        self.persistant_next_ifid.append(self.next_ifid)
        self.persistant_next_memwb.append(self.next_memwb)
        
        self.ifid = self.next_ifid
        self.idex = self.next_idex
        self.exmem = self.next_exmem
        self.memwb = self.next_memwb
        
        self.next_ifid = []
        self.next_idex = []
        self.next_exmem = []
        self.next_memwb = []
    
    def print(self):
        return
    
    