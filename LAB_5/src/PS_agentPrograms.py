#How do we decide which node from the frontier to expand next?
from src.nodeClass import Node
from queue import PriorityQueue

nodeColors={
    "start":"red",
    "goal": "green",
    "frontier": "orange",
    "expanded":"pink"
}

  
#   L/R = 2
#   D = 1
#   U = 4

def BestFirstSearchAgentProgram(f=None):  
    if f is None:
        def f(node):
            total_cost = 0
            path = node.path()
            print()
            for i in range(1, len(path)):
                print(path[i].action, " -> ", end="")
                if path[i].action == "left" or path[i].action == "right":
                    total_cost += 2
                elif path[i].action == "up":
                    total_cost += 4
                elif path[i].action == "down":
                    total_cost += 1
            print("TOTAL_COST: ", total_cost)
            return total_cost
                
    
    def program(problem):
      node = Node(problem.initial)
      #node.color=nodeColors["start"]
      #print(node.state)
      frontier = PriorityQueue()
      frontier.put((f(node),node))
      print(f"The {node} is being pushed to frontier ...")
      #node.color=nodeColors["frontier"]
      reached = {problem.initial:node}

      while frontier:
        node = frontier.get()[1]
        #node.color=nodeColors["expanded"]
        print(f"The {node} is being extracted from frontier ...")
        
        
        # check for Alien
        # node.state = (x, y) location

        if problem.goal_test(node.state):
          node.color=nodeColors["goal"]
          print(f"\033[32mWe have found our goal:  {node}!\033[0m")
          return node
        #reached.add(node.state)
        for child in node.expand(problem):
            if child.state not in reached or child.path_cost<reached[child.state].path_cost:
                frontier.put((f(child),child))
                print(f"The child {child} is being pushed to frontier ...")
                #child.color=nodeColors["frontier"]
                reached.update({child.state:child})
            
        #node.color=nodeColors["expanded"]
      return None
    
    return program




def IDSearchAgentProgram(f=None):
    def program(problem):
        depth = 0
        while True:
            result = DLS(problem, depth)
            if result != 'cutoff':
                return result
            depth += 1

    def DLS(problem, limit):
        return RecursiveDLS(Node(problem.initial), problem, limit)

    def RecursiveDLS(node, problem, limit):
        if problem.goal_test(node.state):
            print(f"\033[32mGoal found: {node}\033[0m")
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                child.depth = node.depth + 1
                result = RecursiveDLS(child, problem, limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            if cutoff_occurred:
                return 'cutoff'
            else:
                return None

    return program






def BestFirstSearchAgentProgramForShow(f=None):
    #with BFS we choose a node, n, with minimum value of some evaluation function, f (n).
    
    def program(problem):
      #print(111)
      steps = 0
      allNodeColors = []
      nodeColors = {k : 'white' for k in problem.graph.nodes()}

      node = Node(problem.initial)
      nodeColors[node.state] = "yellow"
      steps += 1
      allNodeColors.append(dict(nodeColors))

      #print(node.state)
      frontier = PriorityQueue()
      frontier.put((1,node))

      nodeColors[node.state] = "orange"
      steps += 1
      allNodeColors.append(dict(nodeColors))



      reached = {problem.initial:node}

      while frontier:
        node = frontier.get()[1]
        nodeColors[node.state] = "red"
        steps += 1
        allNodeColors.append(dict(nodeColors))
        #print(node)

        if problem.goal_test(node.state):
          nodeColors[node.state] = "green"
          steps += 1
          allNodeColors.append(dict(nodeColors))
          return (node,steps,allNodeColors)
          

        #reached.add(node.state)
        for child in node.expand(problem):
            if child.state not in reached or child.path_cost<reached[child.state].path_cost:
                frontier.put((1,child))
                nodeColors[child.state] = "orange"
                steps += 1
                allNodeColors.append(dict(nodeColors))

                reached.update({child.state:child})

        # modify the color of explored nodes to blue
        nodeColors[node.state] = "blue"
        steps += 1
        allNodeColors.append(dict(nodeColors))
            
      return None

    return program