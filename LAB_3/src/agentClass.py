#This subclass of a base Thing class represents an Agent
'''It has one required slot (attribute), .program, which reperesents Agent Program (the Core of Agent's logic).
Agent Program should hold a function that takes one argument, the Percept, and returns an action.'''

'''!!! Note that '.program' is a slot, not a method.
If it were a method, then the program could 'cheat' and look at aspects of the agent.
It's not supposed to do that: the program can only look at the percepts'''

'''
There is an optional slot, .performance, which is a number giving
the performance measure of the agent in its environment.'''
from src.thingClass import Thing

from collections.abc import Callable  #we need collections.abc which provides abstract base classes that can be used to test whether a class provides a particular interface

from src.food import *

from src.Task3YourClasses import *

class Agent(Thing):

    def __init__(self, program=None):
        self.alive = True
        self.performance = 6
        self.location=None

        if program is None or not isinstance(program, Callable):
            print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))

        self.program = program
        
# TODO: Check if cat needs to eat or drink depending on isinstance food subclass
class Cat(Agent):
    def action(self, food):
        if isinstance(food, Milk):
            self._drink(food)
        elif isinstance(food, Sausage):
            self._eat(food)
           
    # Do not call directly 
    def _drink(self, food):
        print(f"Cat drank {food.weight}g and {food.calories}cal ")
        
    # Do not call directly
    def _eat(self, food):
        print(f"Cat ate {food.weight}g and {food.calories}cal ")
        
    def is_alive(self):
        return self.alive
    
    def show_state(self):
        print(f"{self.__class__.__name__}: Alive: {self.alive}, Perf: {self.performance}, Loc: {self.location}")

class DeliveryMan(Agent):
    def action(self, person, item):
        if isinstance(item, Pizza):
            self.give(Student(person), Pizza)
        elif isinstance(item, Mail):
            self.give(OfficeManager(person), Mail)
        elif isinstance(item, Donuts):
            self.give(ITStaff(person), Donuts)
            
    def give(self, person, item):
        pass