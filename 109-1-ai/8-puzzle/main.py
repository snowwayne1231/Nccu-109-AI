from status import PuzzleState

if __name__ == "__main__":
    print('Start')
    
    state_start = PuzzleState(square_num=9)
    state_goal = PuzzleState(square_list=[
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5],
    ])

    print('state_start: ', state_start)
    print('state_goal: ', state_goal)