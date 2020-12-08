from agents import EightPuzzleSolvingAgent
from states import UniqueNumberSquareState
from enums import SearchModeEnum
import sys, getopt


def enter_input_mode():
    _static_choices = [
        ('Iterative-Deepening Search (IDS) ', SearchModeEnum.IDS),
        ('Uniform-Cost Search', SearchModeEnum.UCS),
        ('Greedy Best-First Search', SearchModeEnum.GREEDY_BFS),
        ('A* Search', SearchModeEnum.A_STAR),
        ('Recursive Best-First Search (RBFS)', SearchModeEnum.RECURSIVE_BFS),
    ]
    print('')
    print('Please Choose A Search Mehtod To Resolve This Problem: ')
    _idx = 1
    for _ in _static_choices:
        key = _[0]
        print('({}). {}'.format(_idx, key))
        _idx += 1
    number = input()
    number = int(number)
    if number < 6 and number > 0:
        return _static_choices[number-1][1]
    else:
        print('Your Choice Is Wrong Number.')
        exit(2)


def get_states_by_operation(operate = 1):
    if operate == 2:
        start = UniqueNumberSquareState(square_num=16)
        goal = UniqueNumberSquareState(square_list=[
            [ 1,  2,  3,  4],
            [12, 13, 14,  5],
            [11,  0, 15,  6],
            [10,  9,  8,  7],
        ])
    else:
        # easier be solved square
        # state_start = UniqueNumberSquareState(square_list=[
        #     [8,3,5],
        #     [4,1,6],
        #     [2,7,0],
        # ])
        start = UniqueNumberSquareState(square_num=9)
        goal = UniqueNumberSquareState(square_list=[
            [1, 2, 3],
            [8, 0, 4],
            [7, 6, 5],
        ])
    return start, goal


def main(argv):

    opts, args = getopt.getopt(argv,":v",["lv"])
    level = 1
    for opt, arg in opts:
        if opt == '-v':
            level = 2

    state_start, state_goal = get_states_by_operation(level)

    print('Start: ')
    print(state_start)
    print('Goal: ')
    print(state_goal)

    MODE = enter_input_mode()

    agent = EightPuzzleSolvingAgent(goal=state_goal, state=state_start, search_mode=MODE)

    ans = agent.search()
    print('Ans: ', ans)
    result = agent.get_result()
    print('Movements: {}   States: {}'.format(len(result[0]), result[1]))
    



if __name__ == "__main__":
    
    try:

        print('-----Start-----')

        main(sys.argv[1:])

        print('----- END -----')

    except KeyboardInterrupt:

        print('')
        print('End Process. By Ctrl-C')
        exit(2)
    

    