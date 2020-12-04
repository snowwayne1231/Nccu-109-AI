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



class UniqueNumberSquareState(BasicState):
    """
    """
    square = None
    x_shape = 0
    y_shape = 0

    def __init__(self, square_list = None, square_num = 0, square = None):
        if square_list:
            self.square = np.array(square_list)
        elif square_num:
            _sq = round(math.sqrt(square_num))
            _square = np.arange(square_num)
            np.random.shuffle(_square)
            self.square = _square.reshape((_sq, _sq))
        elif isinstance(square, np.ndarray):
            self.square = np.copy(square)
        else:
            self.square = np.array([])
        
        _shape = self.square.shape
        
        self.y_shape = int(_shape[0])
        self.x_shape = int(_shape[1])
    

    def get_location(self, label):
        x = 0
        y = 0
        while (y < self.y_shape):
            _line = self.square[y]
            if label in _line:
                x = np.where(_line == label)[0]
                return x, y
            y += 1
        return -1, -1
    

    def get_hash(self):
        count = int(0)
        sum = int(0)
        _length = (self.x_shape*self.y_shape)
        for i in self.square.flatten():
            sum += i * math.pow(_length, count)
            count += 1
        return int(sum)


    def check_in_square(self, x, y):
        return x >= 0 and y >= 0 and x < self.x_shape and y < self.y_shape

    
    def switch_zero(self, zero_position, next_position):
        self.square[zero_position[1], zero_position[0]] = self.square[next_position[1], next_position[0]]
        self.square[next_position[1], next_position[0]] = 0
        return self


    @classmethod
    def clone(cls, status):
        return cls(square=status.square)
    

    def __str__(self):
        return (self.square.__str__())
    

    def __eq__(self, other):
        if(other == None):
            return False
        return np.array_equal(self.square, other.square)