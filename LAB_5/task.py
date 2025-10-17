from src.mazeData import makeMaze
from src.mazeData import defineMazeActions
from src.mazeData import defineMazeAvailableActions
from src.mazeData import makeMazeTransformationModel
from src.graphProblemClass import GraphProblem
from src.maze2025GraphClass import mazeGraph
from src.mazeData import mazeStatesLocations
from pyvis.network import Network
from src.mazeData import intTupleTostr
from src.mazeProblemClass import MazeProblem
from src.PS_agentPrograms import BestFirstSearchAgentProgram
from src.agents import ProblemSolvingMazeAgentBFS
from src.naigationEnvironmentClass import MazeNavigationEnvironment
from src.problemClass import Problem
from src.nodeClass import Node

def search_helper(node):
    return node.path_cost



def main():
    # generate 7x7 maze
    # 25% asteroid (walls)
    # 10% enemies
    maze = makeMaze(7)
    #print(maze)
    
    mazeALLActs = defineMazeActions(maze)
    #print(mazeALLActs)
    
    # all available actions defined for random generated maze at runtime
    mazeAvailableActs = defineMazeAvailableActions(maze)
    #print(mazeAvailableActs)
    
    # make transformation model according to available acts
    mazeTM = makeMazeTransformationModel(mazeAvailableActs)
    #for key in mazeTM:
        #print(f"{key}: ", end="")
        #print(mazeTM[key])
    #print(mazeTM)
        
    mazeWorldGraph = mazeGraph(mazeTM, mazeStatesLocations(list(mazeTM.keys())))
    
    net_maze = Network( heading="Lab4. Examples of Maze World Problem",
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%" 
    ) 
    
    nodeColors={
        "wall":"red",
        "path": "white"
    }
    
    nodeColorsList=[]

    for node in mazeWorldGraph.origin.keys():
        if maze[node[0],node[1]]==1:
            nodeColorsList.append(nodeColors["path"])
        else:
            nodeColorsList.append(nodeColors["wall"])
    nodeColorsList
    
    nodes=["-".join(str(item) for item in el) for el in mazeWorldGraph.origin.keys()]

    x_coords = []
    y_coords = []

    for node in mazeWorldGraph.origin.keys():
        x,y=mazeWorldGraph.getLocation(node)
        x_coords.append(x)
        y_coords.append(y)
        
    sizes=[10]*len(nodes)
    net_maze.add_nodes(nodes, color=nodeColorsList, x=x_coords, y=y_coords, size=sizes, title=nodes)
    
    for node in net_maze.nodes:
        node['label']=''
        
    mazeWorldGraph.origin[(0,0)]
    intTupleTostr((0,0))
    
    edge_weights = {(intTupleTostr(k), intTupleTostr(v2)) : k2 for k, v in mazeWorldGraph.origin.items() for k2, v2 in v.items()}
    
    edges=[]

    for node_source in mazeWorldGraph.nodes():
        for node_target, action in mazeWorldGraph.get(node_source).items():
            #node_target or node_source is a tuple -> convert to str
            if (intTupleTostr(node_source),intTupleTostr(node_target)) not in edges and (intTupleTostr(node_target), intTupleTostr(node_source)):
                net_maze.add_edge(intTupleTostr(node_source),intTupleTostr(node_target), label=edge_weights[(intTupleTostr(node_source),intTupleTostr(node_target))])
                edges.append((intTupleTostr(node_source),intTupleTostr(node_target)))
    
    net_maze.toggle_physics(False)
    net_maze.show("graph1.html", notebook=False)
    
    
    
    
    mazeEnv = MazeNavigationEnvironment(mazeWorldGraph)
    mazeEnv.generateAliens(maze, 4)
    #print("Tryinig to print")
    #mazeEnv.printAlienLocations()
    
    initState, goalState = mazeEnv.genInitGoalState(maze)
    
    mazeProblem = MazeProblem(initState,goalState,mazeWorldGraph)
    testState=(0,2)
    
    # tests state
    #mazeProblem.actions(testState)
    
    problem = Problem(initState, goalState)
    node = Node(problem.initial)
    #BFSAP1=BestFirstSearchAgentProgram()
    #print(mazeProblem.initial)
    
    #seq=BFSAP1(mazeProblem)
    #print(seq)
    
    BFS_MazeAgent = ProblemSolvingMazeAgentBFS(initState, mazeWorldGraph, goalState)
    #print(BFS_MazeAgent.goal)
    
    nodeColors.setdefault('goal', "green")
    nodeColors.setdefault('init', "gold")
    nodeColors.setdefault('alien', 'purple')
    
    for node in net_maze.nodes:
        node_id = node['id']
        if node_id == intTupleTostr(goalState):
            node['color'] = nodeColors['goal']
        elif node_id == intTupleTostr(initState):
            node['color'] = nodeColors['init']
        else:
            # Check all aliens’ locations
            for alien in mazeEnv.aliens:
                if node_id == intTupleTostr(alien.location):
                    node['color'] = nodeColors['alien']
                    break  # Stop checking once you find a match
    
    net_maze.show("asteroidField.html", notebook=False)
    
    mazeEnv.add_thing(BFS_MazeAgent)
    #print("AGENT STATE: ", BFS_MazeAgent.state)
    
    
    # visualize maze environment with HTML
    # cells occupied by enemy are availble to visit (not blocked)
    # enemy is subclass of Thing
        # power attribute random [10% - 40%]
    # four actions of spaceship (up, down, left, right)
    
    # develop transition model
    # location of enemies are unkown
    
    # IF agent contacts enemy with power 2x agent performance, agent dies
    # IF agent contacts enemy, may use 10% performance to defend it if available
        # while in defence mode, agent may move through cell containing enemy
        
    # 2 satellite agents (uniform-cost & iterative DLS)
    # must fully implement IDLS

    #print("GOAL STATE: ", goalState)
    #mazeEnv.run()
    
    mazeEnv.printAlienLocations()
    
    i = 1
    while BFS_MazeAgent.alive:
        print("Step ", i)
        mazeEnv.step(mazeTM)
        BFS_MazeAgent.location = BFS_MazeAgent.location  # Update agent location to match its state
        print(f"Agent location: {BFS_MazeAgent.location}")
        print(f"Agent Performance: {BFS_MazeAgent.performance}")
        i += 1
        
    print("End simulation")

main()
