class Pipelines:
    read_pipe = []
    write_pipe = []
    execute_pipe = []

    def check(self):
        if(len(self.read_pipe) == 0 and len(self.write_pipe) == 0 and len(self.execute_pipe) == 0):
            return True
        return False