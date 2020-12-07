from enums import SearchEightPuzzleDirection
from states import UniqueNumberSquareState


class BasicProblem():
    """
    """
    ACTIONS = {
        'LEFT': 'MOVE_LEFT',
        'RIGHT': 'MOVE_RIGHT',
    }

    state_start = None
    state_goal = None
    state_hash_map = {}

    def __init__(self, start, goal):
        self.state_start = start
        self.state_goal = goal
    
    def get_initial(self):
        return self.state_start

    def get_goal(self):
        return self.state_goal

    def test_goal(self, state):
        return state == self.state_goal




class EightPuzzleProblem(BasicProblem):
    """
    """

    ACTIONS = {
        'UP': SearchEightPuzzleDirection.UP,
        'DOWN': SearchEightPuzzleDirection.DOWN,
        'LEFT': SearchEightPuzzleDirection.LEFT,
        'RIGHT': SearchEightPuzzleDirection.RIGHT,
    }


    def get_next_state_by_action(self, action, state = None):
        if state is None:
            state = self.state_start

        _param = self.getParamByActionName(action)
        if _param:
            return self.getStateWithMoveXY(state=state, moveX=_param[0], moveY=_param[1])
        else:
            return None


    def get_actions_without_opposite(self, action_key):
        _opposite_key = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT',
        }
        _fixed = _opposite_key.get(action_key)
        return {k: self.ACTIONS[k] for k in self.ACTIONS if k != _fixed} 

        
    
    @staticmethod
    def getParamByActionName(name):
        _action_params = {
            SearchEightPuzzleDirection.UP : (0, -1),
            SearchEightPuzzleDirection.DOWN : (0, 1),
            SearchEightPuzzleDirection.LEFT : (-1, 0),
            SearchEightPuzzleDirection.RIGHT : (1, 0),
        }
        return _action_params.get(name)


    @staticmethod
    def getStateWithMoveXY(state, moveX, moveY):
        zero_x, zero_y = state.get_location(0)
        next_x = zero_x + moveX
        next_y = zero_y + moveY
        if state.check_in_square(x=next_x, y=next_y):
            next_state = state.clone(state)
            return next_state.switch_zero(zero_position=(zero_x, zero_y), next_position=(next_x, next_y))
        else:
            return None
    


    


        
