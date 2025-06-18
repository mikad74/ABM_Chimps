class Agent:
    def __init__(self):
        self.pos = (0,0)
    
    @property
    def X(self):
        return self.pos[0]

    @property
    def Y(self):
        return self.pos[1]
