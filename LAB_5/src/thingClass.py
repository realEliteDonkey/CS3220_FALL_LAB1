import random

class Thing:
    # no constructor
    
    def __repr__(self):
        return f"{self.__class__.__name__}"
    

class Alien(Thing):
    def __init__(self, location):
        super().__init__()
        self.location = location
        # performance in range of 10-40% of agent init performance
        self.power = random.randint(int((0.10) * 49), int((0.40) * 49))