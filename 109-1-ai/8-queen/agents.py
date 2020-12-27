from states import SquareState
from problems import EightQueenProblem
from enums import SearchModeEnum, SearchStatus
from searchs import IterativeDeepeningSearch, UniformCostSearch, GreedyBestFirstSearch, AStarSearch, RecursiveBestFirstSearch



class BasicAgent():
    """

    """
    sequence = []
    percept = {}
    state = None
    goal = None
    problem = None

    def __init__(self, percept = {}, state = None, goal = None, problem = None):
        self.percept = percept
        self.problem = problem
        self.state = state
        self.goal = goal


class EightQueenSolvingAgent(BasicAgent):
    """
        
    """

    model_search = None

    def __init__(self, state, search_mode:SearchModeEnum, percept={}):
        super().__init__(state=state, percept=percept)
        self.check_problem()
        self.check_search_by_mode(search_mode)
    

    def search(self):
        _searched = self.model_search.search()
        if _searched == SearchStatus.SOLUTION:
            self.sequence = self.model_search.get_resolved_actions()
            print('')
            # print('Search Successful!  Action movement length: {}  node length: {}'.format(len(self.sequence), self.model_search.num_nodes))
        else:
            self.sequence = []
        return _searched


    def get_result(self):
        return self.sequence, self.model_search.num_nodes

    
    def get_goal_node(self):
        return self.model_search.node_goal


    def check_problem(self):
        if self.problem is None:
            self.problem = EightQueenProblem(start=self.state)
        return self


    def check_search_by_mode(self, mode):
        if mode == SearchModeEnum.IDS:
            self.model_search = IterativeDeepeningSearch(problem=self.problem)

        elif mode == SearchModeEnum.UCS:
            self.model_search = UniformCostSearch(problem=self.problem)

        elif mode == SearchModeEnum.GREEDY_BFS:
            self.model_search = GreedyBestFirstSearch(problem=self.problem)

        elif mode == SearchModeEnum.A_STAR:
            self.model_search = AStarSearch(problem=self.problem)

        elif mode == SearchModeEnum.RECURSIVE_BFS:
            self.model_search = RecursiveBestFirstSearch(problem=self.problem)

        return self




