from states import BasicState


class Node:
    """
    """
    parent = None
    children = []
    action = ''
    state = None
    depth = 0
    score = 0
    cost = 0
    f = 0

    def __init__(self, state, parent = None, action = '', depth:int = 0, score:float = 0, cost:float = 0):
        self.parent = parent
        self.action = action
        self.state = state
        self.depth = depth
        self.score = score
        self.cost = cost
    

    def get_neighbors(self):
        return [_ for _ in self.parent.children if _ != self]

    
    def set_children(self, children_list):
        self.children = children_list
        return self
    

    def __eq__(self, other):
        return other.state.get_hash() == self.state.get_hash()


    def __str__(self):
        return self.state.get_hash()


