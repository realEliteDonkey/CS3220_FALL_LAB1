from environmentClass import *
from catFriendlyHouse import *
from task2_rules import *
from agentPrograms import TableDrivenAgentProgram
from agentClass import *



def main():
    # create environment
    env = CatFriendlyHouse()
    # drop agent into environment
    env.add_thing(Cat(TableDrivenAgentProgram(feeding_rules))) 
    
    for rule in feeding_rules:
        print(rule)
    # step through environment and display logs
    env.run(50)
    #
    
    

main()