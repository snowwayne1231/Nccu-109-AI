from agents import EightPuzzleSolvingAgent
from states import UniqueNumberSquareState
from enums import SearchModeEnum

if __name__ == "__main__":
    print('Start')

    
    state_start = UniqueNumberSquareState(square_num=9)
    state_goal = UniqueNumberSquareState(square_list=[
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5],
    ])

    print('state_start: ', state_start)
    print('state_goal: ', state_goal)

    first_agent = EightPuzzleSolvingAgent(goal=state_goal, state=state_start, search_mode=SearchModeEnum.IDS)
    _ans_1 = first_agent.search()
    print('_ans_1: ', _ans_1)

    print('END-----state_start: ', state_start)
    print('END-----state_goal: ', state_goal)

    