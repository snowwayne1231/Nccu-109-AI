import math, random 
import numpy as np



class BasicState():
    
    name = ''

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if(other == None):
            return False
        return self.name == other.name


class SquareState(BasicState):
    """
        方形棋盤矩陣
    """
    square = None
    x_shape = 0
    y_shape = 0
    now_queen = 0
    max_queen = 0
    last_queen_position = (0,0)


    def __init__(self, width=0, height=0, max_queen = 0, now_queen=0, square=None):
        if width > 0 and height > 0:
            self.square = np.zeros((width, height), dtype=int)
        elif square is not None:
            self.square = np.copy(square)

        _shape = self.square.shape
        self.y_shape = int(_shape[0])
        self.x_shape = int(_shape[1])
        self.max_queen = max_queen

        if now_queen == 0:
            random_y = random.randint(0, height-1)
            random_x = random.randint(0, width-1)
            self.put_queen(x=random_x, y=random_y)
        else:
            self.now_queen = now_queen


    def check_no_conflict(self, x, y):
        _i = 0
        while (_i < self.y_shape):
            if self.square[_i][x] == 1:
                return False
            _y_gap = abs(_i - y)
            _left = x - _y_gap
            _right = x + _y_gap
            if _left >= 0 and self.square[_i][_left] == 1:
                return False
            if _right < self.x_shape and self.square[_i][_right] == 1:
                return False
            _i += 1

        _i = 0
        while (_i < self.x_shape):
            if self.square[y][_i] == 1:
                return False
            _x_gap = abs(_i - x)
            _top = y - _x_gap
            _bottom = y + _x_gap
            if _top >= 0 and self.square[_top][_i] == 1:
                return False
            if _bottom < self.y_shape and self.square[_bottom][_i] == 1:
                return False
            _i += 1

        return True



    def put_queen(self, x, y):
        _move_y = 0
        while (_move_y < self.y_shape):
            _move_x = 0
            _gap_y = abs(y - _move_y)
            _is_horizontal = _gap_y == 0
            while (_move_x < self.x_shape):
                _gap_x = abs(x - _move_x)
                _is_vertical = _gap_x == 0
                _is_slope = _gap_y == _gap_x # 斜率1
                if _is_horizontal or _is_vertical or _is_slope: 
                    if self.square[_move_y][_move_x] == 1:
                        return False
                    self.square[_move_y][_move_x] = -1

                _move_x += 1
            _move_y += 1
        
        self.square[y][x] = 1
        self.now_queen += 1
        self.last_queen_position = (y,x)

        return True


    def get_hash(self):
        _list = []
        _i = 0
        while (_i < self.y_shape):
            _x_line = self.square[_i]
            _idx_x = 0
            if 1 in _x_line:
                _idx_x = list(_x_line).index(1) + 1
            
            _list.append(str(_idx_x))
            _i += 1
        return ''.join(_list)


    def queen_result(self):
        result = np.copy(self.square)
        for _y_idx, _y in enumerate(result):
            for _x_idx, _x in enumerate(_y):
                if  _x == -1:
                    result[_y_idx][_x_idx] = 0
        return result
    
    

    @classmethod
    def clone(cls, status):
        return cls(square=status.square, max_queen=status.max_queen, now_queen=status.now_queen)


    def __str__(self):
        return (self.square.__str__())
    

    def __eq__(self, other):
        if(other == None):
            return False
        return np.array_equal(self.square, other.square)




