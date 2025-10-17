from src.environmentClass import Environment
from src.thingClass import Alien
import random
from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
from src.mazeProblemSolvingAgentSMARTClass import MazeProblemSolvingAgentSMART

class MazeNavigationEnvironment(Environment):
  def __init__(self, navGraph):
    super().__init__()
    self.status = navGraph
    self.aliens = []
    
    
    
  
  # Generates enemy in empty space in maze
  # assigned enemy location to self.enemyLoc
  # auto adds thing to environment
  def generateAliens(self, maze, numAliens):
    max_enemies = numAliens
    current = 0
    while current < max_enemies:
      row = random.randint(0, 6)
      col = random.randint(0, 6)
      if maze[row][col] == 1:
        current += 1
        self.aliens.append(Alien((row, col)))
        
  def genInitGoalState(self, maze):
    init = None
    goal = None
    while init is None or goal is None:
      row = random.randint(0, 6)
      col = random.randint(0, 6)
      if maze[row][col] == 1:
        if init is None:
          if goal is not (row, col):
            init = (row, col)
        elif goal is None:
          if init is not (row, col):
            goal = (row, col)
    
    return init, goal
          
          
          
  def printAlienLocations(self):
    print("Aliens: ", end="")
    for alien in self.aliens:
      print(alien.location, end=", ")
    
    

  def percept(self, agent):
    #Returns the agent's location, and the location status (Dirty/Clean).
    return agent.state

  def is_agent_alive(self, agent: SimpleProblemSolvingAgentProgram):
    return agent.alive

  def update_agent_alive(self, agent: SimpleProblemSolvingAgentProgram):
    if agent.performance <= 0:
      agent.alive = False
      print("Agent {} is dead.".format(agent))
    elif agent.state==agent.goal or len(agent.seq)==0:
      agent.alive = False
      if len(agent.seq)==0:
        print("\033[32mAgent reached all goals\033[0m")
      else:
        print(f"\033[32mAgent reached the goal: {agent.goal}\033[0m")
      

  def execute_action(self, agent: MazeProblemSolvingAgentSMART, action, TM: dict):
    '''Check if agent alive, if so, execute action'''
    if self.is_agent_alive(agent):
        """Change agent's location -> agent's state;
        Track performance.
        -1 for each move."""
        agent.state = agent.update_state(action, TM)
        agent.performance -= 1
        self.update_agent_alive(agent)
              
        
        # if action == 'Right':
        #     agent.location = loc_B
        #     agent.performance -= 1
        #     self.update_agent_alive(agent)
        # elif action == 'Left':
        #     agent.location = loc_A
        #     agent.performance -= 1
        #     self.update_agent_alive(agent)
        # elif action == 'Suck':
        #     if self.status[agent.location] == 'Dirty':
        #         agent.performance += 10
        #     self.status[agent.location] = 'Clean'

  # def default_location(self, thing):
  #       """Agents start in either location at random."""
  #       print("Agent is starting in random location...")
  #       return random.choice([loc_A, loc_B])
  
  def step(self, TM: dict):
    if not self.is_done():
        actions = []
        for agent in self.agents:
          if agent.alive:
            #with agent.state because for PS Agent we don't need to percive
            if not agent.seq:
              return
            action=agent.seq.pop(0)
            print("Agent decided to do {}.".format(action))
            actions.append(action)
            
            for alien in self.aliens:
              if agent.location == alien.location:
                if alien.power >= (2 * agent.performance):
                  print("\033[31mAlien destroyed spaceship\033[0m")
                  agent.performance = 0
                else:
                  print("\033[31mAlien damaged spaceship: -10%\033[0m")
                  agent.performance = int(agent.performance * 0.90)
          else:
            actions.append("")
            
        for (agent, action) in zip(self.agents, actions):
          self.execute_action(agent, action, TM)
    else:
        print("There is no one here who could work...")
    