from agents import EightQueenSolvingAgent
from states import SquareState
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


def get_states_by_num_queen(num_queen = 8):
    return SquareState(width=num_queen, height=num_queen, max_queen=num_queen)


def main(argv):

    opts, args = getopt.getopt(argv,":s",["size"])
    num_queen = 8
    for opt, arg in opts:
        if opt == '-s':
            num_queen = int(args[0])

    print('Queen Size: ', num_queen)

    MODE = enter_input_mode()
    # MODE = SearchModeEnum.IDS
    
    state_init = get_states_by_num_queen(num_queen=num_queen)
    poisition_init = state_init.last_queen_position

    print('Start State: ')
    print(state_init)

    agent = EightQueenSolvingAgent(state=state_init, search_mode=MODE)

    ans = agent.search()
    print('Ans: ', ans)

    goal_node = agent.get_goal_node()
    if goal_node:
        print("Goal State: ")
        print(goal_node.state.queen_result())
    
    actions, state_space = agent.get_result()
    print('Movements: {}   States: {}'.format(len(actions), state_space))
    print('first position: ', poisition_init)
    print('action positions: ', actions)

    
    



if __name__ == "__main__":
    
    try:

        print('---------------Start---------------')

        main(sys.argv[1:])

        print('--------------- END ---------------')

    except KeyboardInterrupt:

        print('')
        print('End Process. By Ctrl-C')
        exit(2)
    

    