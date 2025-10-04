from src.environmentClass import Environment
from src.locations import *
from src.food import *

import random

class CatFriendlyHouse(Environment):
    
    def __init__(self):
        super().__init__()
        
        self.status = {
            loc_A: "Empty",
            loc_B: "Empty"
        }
        
        choice = random.randint(0, 1)
        if choice == 0:
            self.status[loc_A] = Milk()
            self.status[loc_B] = Sausage()
        else:
            self.status[loc_A] = Sausage()
            self.status[loc_B] = Milk()
    
    # returns a tuple of location and status
    def percept(self, agent):
        loc = agent.location
        if loc == loc_A:
            loc_str = 'A'
        else:
            loc_str = 'B'
        content = self.status[loc]
        if isinstance(content, Milk):
            content_str = 'MilkHere'
        elif isinstance(content, Sausage):
            content_str = 'SausageHere'
        else:
            content_str = 'Empty'
        return (loc, content_str)
        
    def default_location(self, thing):
        return random.choice([loc_A, loc_B])
    
    def is_done(self):
        return not any(agent.is_alive() for agent in self.agents)
        
    
    def is_agent_alive(self, agent):
        if agent.alive:
            return True
        return False
    
    def update_agent_alive(self, agent):
        if agent.performance <= 0:
            agent.alive = False
            print("Agent {} is dead.".format(agent))
    
    def execute_action(self, agent, action):
        # Update agent
        # Update environment
        if self.is_agent_alive(agent):
            if action == "MoveRight":
                if agent.location == loc_A:
                    agent.location = loc_B
                    agent.performance -= 1
                    self.agent_stats(agent)
                    self.update_agent_alive(agent)
            elif action == "MoveLeft":
                if agent.location == loc_B:
                    agent.location = loc_A
                    agent.performance -= 1
                    self.agent_stats(agent)
                    self.update_agent_alive(agent)
            elif action == "Eat":
                #           (Food() instance)
                agent.action(self.status[agent.location])
                agent.performance += 3
                self.agent_stats(agent)
                self.status[agent.location] = "Empty"
            elif action == "Drink":
                agent.action(self.status[agent.location])
                agent.performance += 3
                self.agent_stats(agent)
                self.status[agent.location] = "Empty"
            else:
                print("Unkown action")
        else:
            print("Agent is dead")
                
    def agent_stats(self, agent):
        print(f"Agent: {agent.location}, Perf: {agent.performance}")
        
    def status_str(self):
        s = ""
        for key in self.status:
            s += str(key) + ": "
            s += str(self.status[key]) + " "
        return s