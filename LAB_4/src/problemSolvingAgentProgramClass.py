class SimpleProblemSolvingAgentProgram:
  #Abstract framework for a problem-solving agent
  def __init__(self, initial_state=None):
        """State is an abstract representation of the state
        of the world, and seq is the list of actions required
        to get to a particular state from the initial state(root)."""
        self.state = initial_state
        self.seq = []#solution.
        
        self.performance=0
        self.alive=True

  def __call__(self, percept, curGoal=None):
      """Formulate a goal and problem, then search for a sequence of actions to solve it."""
      print("Enter call")

      # Update state
      self.state = self.update_state(self.state, percept)

      # Only search if no current plan
      if not self.seq:
            print("Enter call 2")
            goal = self.formulate_goal(self.state)

            # Handle multiple goals
            if isinstance(goal, list) and len(goal) > 1:
                  print("Enter call 3")
                  for current_goal in goal:
                        print(f"Processing goal: {current_goal}")
                        problem = self.formulate_problem(self.state, current_goal)
                        plan = self.search(problem)
                        if plan:
                              self.seq.extend(plan)
                              self.performance -= len(plan)
                              self.state = plan[-1]
                              print(f"CURRENT STATE = {self.state}")
            else:
                  print("Enter call 4")
                  problem = self.formulate_problem(self.state, goal)
                  self.seq = self.search(problem)

            # No plan found
            if not self.seq:
                  return None
      else:
            print("I have already done my work. Find someone else")

      # Return next action
      return self.seq.pop(0) if self.seq else None

  def update_state(self, state, percept):
        print("Attempted to implement update_state")
        

  def formulate_goal(self, state):
        raise NotImplementedError

  def formulate_problem(self, state, goal):
        raise NotImplementedError

  def search(self, problem):
        raise NotImplementedError