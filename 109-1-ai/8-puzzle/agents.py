from states import UniqueNumberSquareState
from problems import EightPuzzleProblem
from enums import SearchModeEnum
from searchs import IterativeDeepeningSearch



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
        return _searched


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
            pass

        elif mode == SearchModeEnum.GREEDY_BFS:
            pass

        elif mode == SearchModeEnum.A_STAR:
            pass

        elif mode == SearchModeEnum.RECURSIVE_BFS:
            pass

        return self