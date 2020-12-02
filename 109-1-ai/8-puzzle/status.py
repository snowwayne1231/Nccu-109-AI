import math, random 
import numpy as np

class PuzzleState:
    """
    """

    square = None
    x_shape = 0
    y_shape = 0

    def __init__(self, square_list = None, square_num = 0):
        if square_list:
            self.square = np.array(square_list)
        elif square_num:
            _sq = round(math.sqrt(square_num))
            _square = np.arange(square_num)
            np.random.shuffle(_square)
            self.square = _square.reshape((_sq, _sq))
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
                x = _line.index(label)
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
    

    def __str__(self):
        return (self.square.__str__())
    

    def __eq__(self, other):
        if(other == None):
            return False
        return np.array_equal(self.square, other.square)