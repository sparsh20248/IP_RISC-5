class Pipelines:
    read_pipe = []
    write_pipe = []
    execute_pipe = []

    def check(self):
        if(len(self.read_pipe) == 0 and len(self.write_pipe) == 0 and len(self.execute_pipe) == 0):
            return True
        return False

    def print(self):
        print("Read Pipe: ", end = "")
        print(self.read_pipe)
        print("Execute Pipe: ", end = "")
        print(self.execute_pipe)
        print("Write Pipe: ", end = "")
        print(self.write_pipe)