from states import UniqueNumberSquareState, BinaraySquareState
from problems import EightPuzzleProblem
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



class EightPuzzleSolvingAgent(BasicAgent):
    """
    """

    default_square_num = 9
    model_search = None

    def __init__(self, goal, search_mode:SearchModeEnum, percept = {}, state = None):
        super().__init__(percept=percept, state=state, goal=goal)
        self.check_status()
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


    def check_status(self):
        if self.state is None or not isinstance(self.state, UniqueNumberSquareState):
            _square_num = self.percept.get('square_num', self.default_square_num)
            self.state = UniqueNumberSquareState(square_num=_square_num)
        return self


    def check_problem(self):
        if self.problem is None:
            self.problem = EightPuzzleProblem(start=self.state, goal=self.goal)
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


    def check_problem(self):
        if self.problem is None:
            self.problem = EightPuzzleProblem(start=self.state, goal=self.goal)
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




