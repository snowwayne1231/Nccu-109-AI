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

    timer_start = None
    timer_times = 0

    def __init__(self, problem, node=None):
        self.problem = problem
        self.timer_start = time.time()
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


    def add_frontier(self, node, order_by='cost'):
        _frontier = self.frontier
        idx = len(_frontier)

        if order_by == 'cost':
            _lambda = lambda a, b : a.cost >= b.cost
        elif order_by == 'score':
            _lambda = lambda a, b : a.score >= b.score
        
        while (idx>0):
            idx -= 1
            if _lambda(node, _frontier[idx]):
                idx += 1
                break

        self.frontier.insert(idx, node)
        return self

    
    def pop_frontier(self):
        if len(self.frontier) >0:
            return self.frontier.pop(0)
        else:
            False


    def replace_frontier(self, node, idx):
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


    def time_print_fn(self, string = '', times = 0):
        if self.timer_times <= 0 or times == 0:
            _tt = time.time()
            _spended_time = (_tt - self.timer_start) * 1000
            _name = self.__class__.__name__
            print('| {} | Searching... [{}]   [Spend: {:.2f}ms]'.format(_name, string, _spended_time), end='\r')
            self.timer_times = times
        else:
            self.timer_times -= 1
        return self
    



class IterativeDeepeningSearch(BasicSearch):
    """
    """
    
    STATUS_CUTOFF = SearchStatus.CUTOFF
    last_depth = 0

    def search(self):
        _depth = 0
        while True:
            _DLS = DepthLimitedSearch(problem=self.problem, limit=_depth, node=self.node)
            result = _DLS.search()
            self.num_nodes += _DLS.num_nodes

            if result != self.STATUS_CUTOFF:
                if result == self.STATUS_SOLUTED:
                    self.node_goal = _DLS.node_goal
                self.last_depth = _depth
                return result
            _depth += 1
            self.time_print_fn(string='Depth: {}'.format(_depth))





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
        self.add_frontier(self.node)

        while True:
            
            node = self.pop_frontier()
            if node:
                if self.problem.test_goal(node.state):
                    self.node_goal = node
                    return self.STATUS_SOLUTED
                
                self.add_explored(node)
                for _child_node in self.expand_node(node, filter_by_explored=True):
                    _index = self.get_index_in_frontier(_child_node)
                    if _index >= 0:
                        if self.frontier[_index].cost > _child_node.cost:
                            self.replace_frontier(_child_node, _index)
                    else:
                        self.add_frontier(_child_node)
            else:
                break

            self.time_print_fn(string='Explored: {}'.format(len(self.explored)), times=500)

        return self.STATUS_FAILURE
            
        



class GreedyBestFirstSearch(BasicSearch):
    """

    """
    
    def search(self):
        self.add_frontier(self.node)

        while True:
            
            node = self.pop_frontier()
            if node:
                if self.problem.test_goal(node.state):
                    self.node_goal = node
                    return self.STATUS_SOLUTED
                
                self.add_explored(node)

                for _child_node in self.expand_node(node, filter_by_explored=True):
                    _index = self.get_index_in_frontier(_child_node)
                    if _index < 0:
                        heuristic = self.problem.get_heuristic(_child_node.state)
                        _child_node.score = heuristic
                        self.add_frontier(_child_node, order_by='score')
            else:
                break

            self.time_print_fn(string='Explored: {}'.format(len(self.explored)), times=500)

        return self.STATUS_FAILURE




class AStarSearch(BasicSearch):
    """

    """
    
    def search(self):
        self.add_frontier(self.node)

        while True:
            
            node = self.pop_frontier()
            if node:
                if self.problem.test_goal(node.state):
                    self.node_goal = node
                    return self.STATUS_SOLUTED
                
                self.add_explored(node)

                for _child_node in self.expand_node(node, filter_by_explored=True):
                    _index = self.get_index_in_frontier(_child_node)
                    heuristic = self.problem.get_heuristic(_child_node.state)
                    _child_node.score = heuristic + _child_node.cost

                    if _index >= 0:
                        if self.frontier[_index].score > _child_node.score:
                            self.replace_frontier(_child_node, _index)
                    else:
                        self.add_frontier(_child_node)

            else:
                break

            self.time_print_fn(string='Explored: {}'.format(len(self.explored)), times=500)

        return self.STATUS_FAILURE





class RecursiveBestFirstSearch(BasicSearch):
    """

    """

    def search(self):
        
        result, limit = self.RBFS(self.node, float('inf'))
        return result


    def RBFS(self, node, f_limit):
        if self.problem.test_goal(node.state):
            self.node_goal = node
            return self.STATUS_SOLUTED, f_limit

        successors = self.expand_node(node)
        if len(successors) == 0:
            return self.STATUS_FAILURE, float('inf')
        
        for s in successors:
            heuristic = self.problem.get_heuristic(s.state)
            s.score = heuristic + s.cost
            s.f = max(node.f, s.score)

        while True:
            successors.sort(key=lambda _: _.f)
            best = successors[0]
            if best.f > f_limit:
                return self.STATUS_FAILURE, best.f

            if len(successors) > 1:
                min_f = min(f_limit, successors[1].f)
            else:
                min_f = f_limit

            result, best.f = self.RBFS(best, min_f)
            if result != self.STATUS_FAILURE:
                return result, min_f

            self.time_print_fn(string='F: {}'.format(min_f), times=500)

        

