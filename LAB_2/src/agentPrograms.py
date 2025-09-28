import random

'''An idea of Random Agent Program is to choose an action at random, ignoring all percepts'''
def RandomAgentProgram(actions):
   return lambda percept: random.choice(actions)

def TableDrivenAgentProgram(table):
    """
    This agent selects an action based on the percept sequence.
    To customize it, provide as table a dictionary of all 
    {percept_sequence:action} pairs.
    """
    percepts = []
    
    def program(percept):
      percepts.append(percept)
      # match the longest seq in table
      for i in range(len(percepts)):
          seq = tuple(percepts[i:])  # slice suffix from i to end
          action = table.get(seq)
          if action is not None:
            return action
      # no match
      print("No such percept sequence in table")
      return None

    return program
  
  
def ReflexAgentProgram(rules,interpret_input,rule_match):
  #This AP takes action based solely on the percept.
    
    def program(percept):
        state = interpret_input_A2pro(percept)
        action = rule_match_A2pro(state, rules)
        return action

    return program


def interpret_input(percept):
  loc, status = percept
  return status


def rule_match(state, rules):
  for key in rules:
    if state in key:
      return rules[key]




#The code below -> for Task3 of the Assignment



from src.locations import *
from src.Task3YourClasses import OfficeManager, ITStaff, Student

def interpret_input_A2pro(percept):
  loc, percepts = percept
  print(percepts,loc, loc_D)
  status='Clear'
  if len(percepts)==0:
    if loc==loc_D:
      status='Last room'
      #print(1)
  else:
    for p in percepts:
      if isinstance(p, OfficeManager):
        return 'Office manager'
      elif isinstance(p, ITStaff):
        return 'IT'
      elif isinstance(p, Student):
        return 'Student'
  print(status)
  return status

def rule_match_A2pro(state, rules):
  return rules[state]