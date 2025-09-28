import random


class Food:
    def __init__(self, calories):
        self.calories = calories
        self.weight = random.randint(1, 5)
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.weight}g, {self.calories}cal"


class Milk(Food):
    # calories remain constant
    # weight may change per instance
    def __init__(self):
        super().__init__(50)


class Sausage(Food):
    # calories remain constant
    # weight may change per instance
    def __init__(self):
        super().__init__(100)

    
