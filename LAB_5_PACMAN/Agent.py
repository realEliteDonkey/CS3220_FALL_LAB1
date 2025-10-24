from Thing import Thing

class Agent(Thing):
    
    def __init__(self, loc):
        self.power = None
        self.loc = loc
        