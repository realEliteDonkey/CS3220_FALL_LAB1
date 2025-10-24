
""" ASSIGNMENT """

# Test changes

# Compare two algorithms :
    # ( 1 ) Refine A* search : output number of nodes expanded & total cost of the path
    # ( 2 ) Implement a different version of A* using "Manhattan Distance Heuristic"
# Visualize the path(s)

# ( 3 ) there are 5 Ghosts (derived class from Thing class) hidden in the Maze
    # (PacMan Agent can't figure out the location of the ghost in advance
    # They are placed in the Maze randomly, not in the start and finish points,
    # the locations of Fixed Food Dots and Ghosts must also be different.

# ( 4 ) The Pac-man Agent must find all Fixed Food Dots and then find the finish point ->
    # 10% of space is food, randomly distributed.
    # a set of goals (the results of task 2 are supposed to be used).
    # The search of Fixed Food Dots must be rational:
    # the 1st 'food' goal must be the most cost-optimal among other Food Dots.
    # Try to design the appropriate heuristic for this case.

# ( 5 ) The initial performance of Agent is 30% of space cells.
    # After reaching a Fixed Food Dot the agent's performance doubles.

# ( 6 ) If the Agent encounters Ghosts (based on its ability to regognize the
    # types of things in the cell during perception), it fights.
    # But only the strong Agent (with performance > 30% of space cells) can win.
    # Otherwise the Agent will be killed by Ghost.
    # If the Agent wins, he will lose 10% of his previous effectiveness after the battle.

# ( 7 ) Implement IDA* search and apply it for tasks 4-5.

""" INITIAL IMPORTS AND GLOBAL VARS """

import pygame # pip install pygame-ce
import random
from A_Star import *

CELL_SIZE = 64
COLS = 11
ROWS = 11
GHOST_COUNT = 5


    

""" ENVIRONMENT """

class Environment:

    def __init__(self):
        # PYGAME
        self.screen_width = CELL_SIZE * COLS
        self.screen_height = CELL_SIZE * ROWS
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.delta = 0
        self.running = False
        pygame.display.set_caption("Pacman Assignment")
        # GRAPH
        self.graph = self.make_base_graph()
        self.place_walls(20)
        self.food_list_min_heap = []
        self.place_food()
        self.goal = self.place_goal()
        self.place_ghosts()
        self.initial_state = self.find_agent_start_pos()
        self.agents = []

    # for each space-bar press, agent steps through pre-determined action
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("Quit pressed")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Enter key pressed")
                    for agent in self.agents:
                        agent.step()

                    self.update()

    def update(self):
        
        for agent in self.agents:
            if agent.loc == agent.current_goal.loc:
                print("Agent reached its next goal")

                # Remove the reached goal
                if agent.goals_min_heap:
                    agent.goals_min_heap.pop(0)
                print(f"Goal Heap Size: {len(agent.goals_min_heap)}")
                for goal in agent.goals_min_heap:
                    print(f"goal loc: {goal.loc}")

                if agent.goals_min_heap:
                    agent.current_goal = agent.goals_min_heap[0]
                    agent.update_goals()
                    print(f"Goal updated to loc: {agent.current_goal.loc}")
                    agent.step_count = 0
                    self.graph[agent.loc[1]][agent.loc[0]] = 0  # clear food from grid
                    agent.search()
                else:
                    print("All food eaten")
                    # Clear last food from grid
                    self.graph[agent.loc[1]][agent.loc[0]] = 0
                    agent.current_goal = Food(self.goal)
                    agent.step_count = 0
                    agent.search()
                    
                
    
        

    def render(self):
        self.screen.fill("black")
        for y in range(ROWS):
            for x in range(COLS):
                if self.graph[y][x] == 1:
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, 'blue', rect)
                elif self.graph[y][x] == 2:
                    center = (x * CELL_SIZE + (CELL_SIZE/2), y * CELL_SIZE + (CELL_SIZE/2))
                    pygame.draw.circle(self.screen, 'white', center, CELL_SIZE/8)
                elif self.graph[y][x] == 3:
                    center = (x * CELL_SIZE + (CELL_SIZE/2), y * CELL_SIZE + (CELL_SIZE/2))
                    pygame.draw.circle(self.screen, 'green', center, CELL_SIZE/4)
                if self.graph[y][x] == 4:
                    rect = pygame.Rect(x * CELL_SIZE + (CELL_SIZE/4),
                                       y * CELL_SIZE + (CELL_SIZE/4),
                                       CELL_SIZE/2, CELL_SIZE/2)
                    pygame.draw.rect(self.screen, 'red', rect)
        self.render_agent()

    def render_agent(self):
        for agent in self.agents:
            x = agent.x
            y = agent.y
            center = (x * CELL_SIZE + (CELL_SIZE / 2), y * CELL_SIZE + (CELL_SIZE / 2))
            pygame.draw.circle(self.screen, 'yellow', center, CELL_SIZE / 2)

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            self.delta = clock.tick(60) / 1000.0
            self.handle_events()
            self.render()
            pygame.display.flip()
        pygame.quit()

    def make_base_graph(self):
        # EMPTY GRAPH WITH BORDER
        graph = []
        for y in range(ROWS):
            row = []
            for x in range(COLS):
                if y == 0 or x == 0:
                    row.append(1)
                elif x == COLS - 1 or y == ROWS - 1:
                    row.append(1)
                else:
                    row.append(0)
            graph.append(row)
        for row in graph:
            print(row)
        return graph

    def place_walls(self, num_walls=25):
        n = num_walls
        while ( n > 0 ) :
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)
            if self.graph[y][x] == 0:
                self.graph[y][x] = 1
                n -= 1
        # FILL OBVIOUS HOLES
        for y in range(1,ROWS-1):
            for x in range(1,COLS-1):
                good_cell = False
                if self.graph[y][x] == 0:
                    if self.graph[y-1][x] == 0 : good_cell = True
                    elif self.graph[y+1][x] == 0 : good_cell = True
                    elif self.graph[y][x-1] == 0 : good_cell = True
                    elif self.graph[y][x+1] == 0 : good_cell = True
                if not good_cell :
                    self.graph[y][x] = 1

    def place_goal(self):
        n = 1
        x = 0
        y = 0
        while ( n > 0 ) :
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)
            if self.graph[y][x] == 0:
                self.graph[y][x] = 3
                n -= 1
        return x,y

    def place_ghosts(self):
        n = GHOST_COUNT
        while n > 0:
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)
            if self.graph[y][x] == 0:
                self.graph[y][x] = 4
                n -= 1

    def find_agent_start_pos(self):
        x = 0
        y = 0
        while True :
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)
            if self.graph[y][x] == 0:
                break
        return x,y

    def add_agent(self, agent):
        agent.graph = self.graph
        self.agents.append(agent)
         
    def place_food(self):
        n = COLS * ROWS // 10
        while ( n > 0 ) :
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)
            if self.graph[y][x] == 0:
                self.graph[y][x] = 2
                n -= 1
                self.food_list_min_heap.append(Food((x, y)))


                
                
""" AGENT """

class Agent:

    def __init__(self, pos, program):
        self.graph = None
        self.loc = pos
        self.x = pos[0]
        self.y = pos[1]
        self.solution = None
        self.program = program
        self.goals_min_heap = []
        self.step_count = 0
        self.performance = 100
        self.current_goal = None
        
    def update_goals(self):
        for food in self.goals_min_heap:
            food.calc_dist(self)
        self.goals_min_heap.sort()
        
    # set goals in priority of closest one using manhatten equation
    def set_goals(self, food_list):
        for food in food_list:
            self.goals_min_heap.append(food)
        for food in self.goals_min_heap:
            food.calc_dist(self)
        self.goals_min_heap.sort()
        for goal in self.goals_min_heap:
            print(f"{goal.loc[0]}, {goal.loc[1]}")
        #self.goals_min_heap.pop(0)
        
    def search(self):
        if self.goals_min_heap:
            self.current_goal = self.goals_min_heap[0]
            self.solution = IDA_Star(self.loc, self.current_goal, self.graph)
        elif self.current_goal:
            # last goal
            # min_heap will be empty already
            self.solution = IDA_Star(self.loc, self.current_goal, self.graph)
        else:
            print("No goals left")
        
        
    def action(self, action_list):
        if not action_list:
            print("No action in list")
            return

        if self.step_count >= len(action_list):
            print("No more steps left")
            return

        next_pos = action_list[self.step_count]
        current = self.loc

        dx = next_pos[0] - current[0]
        dy = next_pos[1] - current[1]

        dir = None
        if dx < 0:
            dir = "left"
        elif dx > 0:
            dir = "right"
        elif dy < 0:
            dir = "up"
        elif dy > 0:
            dir = "down"

        # update position
        self.loc = next_pos
        self.x, self.y = next_pos
        self.step_count += 1

        print(f"Pacman moved {dir} to {self.loc}")
        
    
    def step(self):
        if self.solution:
            self.action(self.solution)
        else:
            print("No solution left")  
    
class Food:
    def __init__(self, loc):
        self.loc = loc
        self.manhatten_dist = None
    
    def calc_dist(self, agent):        
        self.manhatten_dist = abs(self.loc[0] - agent.x) + abs(self.loc[1] - agent.y)
        return self.manhatten_dist
    
    def __lt__(self, other):
        return self.manhatten_dist < other.manhatten_dist
    
    def __gt__(self, other):
        return self.manhatten_dist > other.manhatten_dist
    

""" RUN THE GAME """

if __name__ == "__main__":
    env = Environment()
    program = None
    pac_agent = Agent(env.initial_state, program)
    env.add_agent(pac_agent)
    pac_agent.set_goals(env.food_list_min_heap)
    pac_agent.search()
    for goal in pac_agent.goals_min_heap:
        print(f"({goal.loc[0]}, {goal.loc[1]})")
    print("Agent loc: ", pac_agent.loc)
    print(f"Current goal: {pac_agent.current_goal.loc}")
    env.run()
    
    

# 1 = wall
# 2 = food
# 3 = goal
# 4 = ghost

# Using agent start position, find food until none left
