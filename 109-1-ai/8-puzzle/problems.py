from enums import SearchEightPuzzleDirection
from states import UniqueNumberSquareState
import math


class BasicProblem():
    """
    """
    ACTIONS = {
        'LEFT': 'MOVE_LEFT',
        'RIGHT': 'MOVE_RIGHT',
    }

    state_start = None
    state_goal = None

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

    goal_flatten_list = []
    goal_zero_x = -1
    goal_zero_y = -1

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


    def init_goal_flatten_list(self):
        self.goal_flatten_list = []
        x_shape = self.state_goal.x_shape
        _list = self.state_goal.square.flatten('C')
        for idx, label in enumerate(_list):
            _x = idx % x_shape
            _y = math.floor(idx/x_shape)
            self.goal_flatten_list.append({
                'x': _x,
                'y': _y,
                'label': label,
            })
            if label == 0:
                self.goal_zero_x = _x
                self.goal_zero_y = _y


    def get_heuristic(self, state):
        if len(self.goal_flatten_list) == 0:
            self.init_goal_flatten_list()

        total = 0
        goal_zero_x = self.goal_zero_x
        goal_zero_y = self.goal_zero_y
            
        for _goal in self.goal_flatten_list:
            need_step = 0
            _goal_x = _goal['x']
            _goal_y = _goal['y']
            _goal_label = _goal['label']

            state_now_x, state_now_y = state.get_location(_goal_label)
            distant_to_goal_x = abs(state_now_x - _goal_x)
            distant_to_goal_y = abs(state_now_y - _goal_y)
            distant_to_zero_x = abs(state_now_x - goal_zero_x)
            distant_to_zero_y = abs(state_now_y - goal_zero_y)

            distant_xy_to_goal = distant_to_goal_x + distant_to_goal_y
            if distant_xy_to_goal == 0:
                continue
            
            move_zero_to_now = distant_to_zero_x + distant_to_zero_y
            need_step += move_zero_to_now

            # evaluate the line move
            if distant_to_goal_x <= 1 and distant_to_goal_y <= 1:
                move_zero_to_goal = ((distant_xy_to_goal-1) * 2) +1
                need_step += move_zero_to_goal

            else:
                if distant_to_goal_x == 0:
                    move = (distant_to_goal_y -1)*5 +1
                elif distant_to_goal_y == 0:
                    move = (distant_to_goal_x -1)*5 +1
                else:
                    move = (distant_xy_to_goal *2) + 1
                need_step += move

            total += need_step

        return total


        

        
    
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


    


    


        
