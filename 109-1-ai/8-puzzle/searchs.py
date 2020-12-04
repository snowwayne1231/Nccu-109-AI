from nodes import Node
from problems import BasicProblem
from enums import SearchStatus


class BasicSearch():
    """

    """
    problem = None
    node = None
    node_goal = None

    def __init__(self, problem, node=None):
        self.problem = problem
        if node is None:
            self.node = Node(state=problem.get_initial())
        else:
            self.node = node

    
    def expand_node(self, node):
        _problem = self.problem
        node_children_list = []
        _actions = _problem.ACTIONS
        for _key in _actions:
            _action_name = _actions[_key]
            _state = _problem.get_next_state_by_action(action=_action_name, state=node.state)
            if _state:
                _new_node = Node(state=_state, parent=node, action=_action_name, depth=node.depth+1, cost=node.cost+1)
                node_children_list.append(_new_node)
        
        node.set_children(node_children_list)
        return node_children_list

    

class IterativeDeepeningSearch(BasicSearch):
    """
    """

    STATUS_SOLUTED = SearchStatus.SOLUTION
    STATUS_CUTOFF = SearchStatus.CUTOFF
    last_depth = 0

    def search(self):
        _depth = 0
        while True:
            print('IterativeDeepeningSearch _depth: ', _depth)
            _DLS = DepthLimitedSearch(problem=self.problem, limit=_depth, node=self.node)
            result = _DLS.search()
            if result != self.STATUS_CUTOFF:
                if result == self.STATUS_SOLUTED:
                    self.node_goal = _DLS.node_goal
                self.last_depth = _depth
                return result
            _depth += 1
            if _depth > 10:
                return self.STATUS_CUTOFF



class DepthLimitedSearch(BasicSearch):
    """
    """
    STATUS_SOLUTED = SearchStatus.SOLUTION
    STATUS_CUTOFF = SearchStatus.CUTOFF
    STATUS_FAILURE = SearchStatus.FAILURE

    def __init__(self, problem, limit, node = None):
        super().__init__(problem=problem, node=node)
        self.limit = limit


    def search(self, limit:int = 0):
        if limit <= 0:
            limit = self.limit
        return self.recursiveDLS(node=self.node, problem=self.problem, limit=limit)


    def recursiveDLS(self, node, problem, limit):
        _cutoff_occurred = False
        if problem.test_goal(node.state):
            self.node_goal = node
            return self.STATUS_SOLUTED
        elif node.depth >= limit:
            return self.STATUS_CUTOFF
        else:
            _expanded_nodes = self.expand_node(node)
            for _sub_node in _expanded_nodes:
                _result = self.recursiveDLS(node=_sub_node, problem=problem, limit=limit)
                if _result == self.STATUS_CUTOFF:
                    _cutoff_occurred = True
                elif _result != self.STATUS_FAILURE:
                    return _result
                    
            if _cutoff_occurred:
                return self.STATUS_CUTOFF
            else:
                return self.STATUS_FAILURE


