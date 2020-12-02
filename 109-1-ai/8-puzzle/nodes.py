from enum import Enum

class Node:
    def __init__(self, parent, action, state, depth: int, score: float = float("inf"), cost: float = float("inf")):
        self.parent = parent
        self.action = action
        self.state = state
        self.depth = depth
        self.score = score
        self.cost = cost
    
    def get_neighbors(self):
        neighbors=[]
        return neighbors
    # This is needed for heap queue
    def __lt__(self, other):
        if(self.score == other.score):
            return self.action < other.action
        else:
            return self.score < other.score



class ProblemHandler:
    ACTIONS = {
        'Up': (0, -1),
        'Down': (0, 1),
        'Left': (-1, 0),
        'Right': (1, 0),
    }
    def __init__ (self,goal_state):
        self.goal_state = goal_state
    def test_goal(self,state): 
        return state == self.goal_state
    def cost(self,node):
        if (node.parent == None):
            return 1
        return node.parent.cost+1
    #Manhatten
    def heuristic(self,state):
        flatten_state = self.goal_state.puzzle_locations.flatten('C')
        sum=0
        for label in flatten_state:
            x_goal,y_goal = self.goal_state.get_location(label)
            x_state,y_state = state.get_location(label)
            sum+=abs(x_goal-x_state)+(y_goal-y_state)
        return sum

    def test_fail(self,state): 
        return False
    def get_successors(self,state):
        result=[]
        for key in PuzzleProblem.ACTIONS.keys():
            action = key
            new_state =PuzzleProblem.transition(state,action)
            if(new_state != None):
                result.append((action,new_state))
        return result
    @staticmethod
    def transition(state: PuzzleState, action):
        new_state = copy.deepcopy(state)
        x_mov, y_mov = PuzzleProblem.ACTIONS[action]
        x_blank, y_blank = new_state.get_location(0)
        x_target = x_blank + x_mov
        y_target = y_blank + y_mov
        if(x_target < 0 or x_target > state.x_size - 1 or y_target < 0 or y_target > state.y_size-1):
            return None
        else:
            new_state.puzzle_locations[y_blank,
                                       x_blank] = new_state.puzzle_locations[y_target, x_target]
            new_state.puzzle_locations[y_target, x_target] = 0
        return new_state

    @staticmethod
    def shuffle(state, steps):
        count = 0
        shuffled_state = state
        while (count < steps):
            action = random.choice(list(PuzzleProblem.ACTIONS.keys()))
            new_state = PuzzleProblem.transition(shuffled_state, action)
            if(new_state != None):
                shuffled_state = new_state
                count += 1
        return shuffled_state