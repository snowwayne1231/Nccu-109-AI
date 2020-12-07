from agents import EightPuzzleSolvingAgent
from states import UniqueNumberSquareState
from enums import SearchModeEnum



def main():

    # state_start = UniqueNumberSquareState(square_num=9)
    state_start = UniqueNumberSquareState(square_list=[
        [8,3,5],
        [4,1,6],
        [2,7,0],
    ])
    # state_start = UniqueNumberSquareState(square_list=[
    #     [1, 2, 3],
    #     [8, 4, 0],
    #     [7, 6, 5],
    # ])
    state_goal = UniqueNumberSquareState(square_list=[
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5],
    ])


    print('Start: ', state_start)
    print('Goal: ', state_goal)

    # agent = EightPuzzleSolvingAgent(goal=state_goal, state=state_start, search_mode=SearchModeEnum.IDS)

    agent = EightPuzzleSolvingAgent(goal=state_goal, state=state_start, search_mode=SearchModeEnum.UCS)


    ans = agent.search()
    print('ans: ', ans)
    result = agent.get_result()
    print('Movements: {}   States: {}'.format(len(result[0]), result[1]))

    

if __name__ == "__main__":
    
    try:

        print('Start')

        main()

        print('-----END-----')

    except KeyboardInterrupt:
        
        print('End Process.. By Ctrl-C')
        exit(2)
    

    