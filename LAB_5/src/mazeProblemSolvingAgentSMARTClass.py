from src.mazeProblemSolvingAgentClass import MazeProblemSolvingAgent
import collections

class MazeProblemSolvingAgentSMART(MazeProblemSolvingAgent):
  def __init__(self, initial_state=None, dataGraph=None, goal=None, program=None, id=None):
    super().__init__(initial_state,dataGraph,goal)
    self.performance=len(dataGraph.nodes()) / 2
    self.location = initial_state
    self.id = id

    if program is None or not isinstance(program, collections.abc.Callable):
      if program is None:
        print("Program is None")
      print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

      def program(percept):
        return eval(input('Percept={}; action? '.format(percept)))

    self.program = program

  def search(self, problem):
    seq = self.program(problem)
    if seq is None:
      print("\033[31mNo path found. Returning empty sequence.\033[0m")
      return []
    solution=self.actions_path(seq.path())
    print(f"Agent {self.id}")
    print("Solution (a sequence of actions) from the initial state to a goal: \n{}".format(solution))
    return solution
  
  def actions_path(self, p):
    acts=[]
    for n in p:
      acts.append(n.action)
    return acts[1:]
  
  def update_state(self, action, TM: dict):
    if self.location not in TM:
        print(f"Agent: {self.id} No transitions found for {self.location}")
        return self.state

    inner_dict = TM[self.location]

    if action in inner_dict:
        new_loc = inner_dict[action]
        print(f"Action {action} moves agent from {self.location} to {new_loc}")
        self.location = new_loc
        self.state = action
    else:
        print(f"Invalid action '{action}' for location {self.location}")

    return self.state