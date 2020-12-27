
from states import SquareState
import math


class BasicProblem():
    """
    """

    state_start = None
    state_goal = None

    def __init__(self, start, goal = None):
        self.state_start = start
        self.state_goal = goal
    
    def get_initial(self):
        return self.state_start

    def get_goal(self):
        return self.state_goal

    def test_goal(self, state):
        return state == self.state_goal



class EightQueenProblem(BasicProblem):
    """
        八皇后問題
    """

    def get_next_empty_line(self, state):
        _y = 0
        while (_y < state.y_shape):
            if 1 in state.square[_y]:
                _y += 1
            else:
                return _y

        return False
    

    def get_all_state_by_horizontal_line_with_prosible(self, line, state = None):
        states = []
        if state is None:
            state = self.state_start

        if line < state.y_shape:
            _this_line = state.square[line]
            if 1 in _this_line:
                return []
            
            for _x_idx, _x_val in enumerate(_this_line):
                if _x_val == 0 and state.check_no_conflict(x=_x_idx, y=line):
                    new_state = state.clone(state)
                    new_state.put_queen(x=_x_idx, y=line)
                    states.append(new_state)

        return states

        
    def test_goal(self, state):
        return state.now_queen == state.max_queen


    def get_heuristic(self, state):
        total_zero = 0
        _y = 0
        _square = state.square
        while (_y < state.y_shape):
            _x = 0
            _line = _square[_y]
            while (_x < state.x_shape):
                if _line[_x] == 0:
                    total_zero += 1
                _x += 1
            _y += 1

        _left_queen = state.max_queen - state.now_queen
        _free_space = total_zero - (_left_queen * 2)
        return max(_free_space, 0)



    



        
