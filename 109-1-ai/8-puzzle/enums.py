from enum import Enum

class SearchModeEnum(Enum):
    IDS = 1
    UCS = 2
    GREEDY_BFS = 3
    A_STAR = 4
    RECURSIVE_BFS = 5



class SearchEightPuzzleDirection(Enum):
    LEFT = 'MOVE_LEFT'
    RIGHT = 'MOVE_RIGHT'
    UP = 'MOVE_UP'
    DOWN = 'MOVE_DOWN'



class SearchStatus(Enum):
    SOLUTION = 1
    CUTOFF = 2
    FAILURE = 0
