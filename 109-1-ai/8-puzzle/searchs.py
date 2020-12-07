from nodes import Node
from problems import BasicProblem
from enums import SearchStatus
import math, time


class BasicSearch():
    """

    """
    STATUS_SOLUTED = SearchStatus.SOLUTION
    STATUS_FAILURE = SearchStatus.FAILURE

    problem = None
    node = None
    node_goal = None
    num_nodes = 0

    frontier = []
    explored = {}

    def __init__(self, problem, node=None):
        self.problem = problem
        if node is None:
            self.node = Node(state=problem.get_initial())
        else:
            self.node = node

    
    def expand_node(self, node, filter_by_explored=False):
        _problem = self.problem
        node_children_list = []
        if node.action:
            _actions = _problem.get_actions_without_opposite(node.action)
        else:
            _actions = _problem.ACTIONS
        
        for _key in _actions:
            _action_name = _actions[_key]
            _state = _problem.get_next_state_by_action(action=_action_name, state=node.state)

            if _state:
                
                if filter_by_explored and self.has_explored(_state.get_hash()):
                    continue
                
                _new_node = Node(state=_state, parent=node, action=_key, depth=node.depth+1, cost=node.cost+1)
                node_children_list.append(_new_node)

        self.num_nodes += len(node_children_list)
        
        node.set_children(node_children_list)
        return node_children_list


    def get_resolved_actions(self):
        _actions = []
        if self.node_goal:
            _now_node = self.node_goal
            while _now_node.parent:
                _actions.append(_now_node.action)
                _now_node = _now_node.parent
        _actions.reverse()
        return _actions


    def add_frontier(self, node):
        _frontier = self.frontier
        _i_frontier = len(_frontier)
        while (_i_frontier>0):
            _i_frontier -= 1
            if node.cost >= _frontier[_i_frontier].cost:
                _i_frontier += 1
                break
        self.frontier.insert(_i_frontier, node)
        return self

    
    def pop_frontier(self):
        if len(self.frontier) >0:
            return self.frontier.pop(0)
        else:
            False


    def replace_frontier(self, idx, node):
        self.frontier.pop(idx)
        self.add_frontier(node)
        self.num_nodes -= 1
        return self


    def get_index_in_frontier(self, node):
        _i = 0
        _frontier = self.frontier
        _len_frontier = len(_frontier)
        while _i < _len_frontier:
            if node == _frontier[_i]:
                return _i
            _i += 1

        return -1

    
    def add_explored(self, node):
        _hash = node.state.get_hash()
        self.explored[_hash] = True
        return self


    def has_explored(self, hash):
        return self.explored.get(hash, False)

    



class IterativeDeepeningSearch(BasicSearch):
    """
    """
    
    STATUS_CUTOFF = SearchStatus.CUTOFF
    last_depth = 0

    def search(self):
        _depth = 0
        self.node_goal = None
        while True:
            _tt = time.time()
            _DLS = DepthLimitedSearch(problem=self.problem, limit=_depth, node=self.node)
            result = _DLS.search()
            self.num_nodes += _DLS.num_nodes

            if result != self.STATUS_CUTOFF:
                if result == self.STATUS_SOLUTED:
                    self.node_goal = _DLS.node_goal
                self.last_depth = _depth
                return result
            _depth += 1
            _tt_end = time.time()
            print('IterativeDeepeningSearch Searching... [Depth: {}]   [Spend: {:.2f}ms]'.format(_depth, (_tt_end-_tt) * 1000), end='\r')





class DepthLimitedSearch(BasicSearch):
    """
    """
    STATUS_CUTOFF = SearchStatus.CUTOFF

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





class UniformCostSearch(BasicSearch):
    """

    """
    
    def search(self):
        _depth = 0
        self.node_goal = None
        self.add_frontier(self.node)
        _tt = time.time()
        _times = 0

        while True:
            
            node = self.pop_frontier()
            if node:
                if self.problem.test_goal(node.state):
                    self.node_goal = node
                    break
                
                self.add_explored(node)
                for _child_node in self.expand_node(node, filter_by_explored=True):
                    _index = self.get_index_in_frontier(_child_node)
                    if _index >= 0:
                        if self.frontier[_index].cost > _child_node.cost:
                            self.replace_frontier(_index, _child_node)
                    else:
                        self.add_frontier(_child_node)
            else:
                break

            if _times > 500:
                # print([_.cost for _ in self.frontier])
                # exit(2)
                _times = 0
                _tt_end = time.time()
                print('UniformCostSearch Searching...  [Spend: {:.2f}ms]  [explored: {}]'.format((_tt_end-_tt) * 1000, len(self.explored)), end='\r')

            _times += 1

        if self.node_goal:
            return self.STATUS_SOLUTED
        else:
            return self.STATUS_FAILURE
            
        



class GreedyBestFirstSearch(BasicSearch):
    """

    """
    
    def search(self):
        _depth = 0
        self.node_goal = None
        self.add_frontier(self.node)
        _tt = time.time()
        _times = 0

        while True:
            
            node = self.pop_frontier()
            if node:
                if self.problem.test_goal(node.state):
                    self.node_goal = node
                    break
                
                self.add_explored(node)
                for _child_node in self.expand_node(node, filter_by_explored=True):
                    _index = self.get_index_in_frontier(_child_node)
                    if _index >= 0:
                        if self.frontier[_index].cost > _child_node.cost:
                            self.replace_frontier(_index, _child_node)
                    else:
                        self.add_frontier(_child_node)
            else:
                break

            if _times > 500:
                # print([_.cost for _ in self.frontier])
                # exit(2)
                _times = 0
                _tt_end = time.time()
                print('UniformCostSearch Searching...  [Spend: {:.2f}ms]  [explored: {}]'.format((_tt_end-_tt) * 1000, len(self.explored)), end='\r')

            _times += 1

        if self.node_goal:
            return self.STATUS_SOLUTED
        else:
            return self.STATUS_FAILURE