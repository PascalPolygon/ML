import os
import sys
from board_utils import BoardUtils
from critic import Critic
from generalizer import Generalizer
from perf_system import PerfSystem
from play_utils import PlayUtils
# Read input file and reprent as gameTrace

DOJO_FILE_PATH = os.getcwd()+'/dojo.txt'

board_utils = BoardUtils()
critic = Critic()
generalizer = Generalizer()
perf_system = PerfSystem()
play_utils = PlayUtils(DOJO_FILE_PATH)

verbose = False
expressivity = 'compact'
lr = 0.001


def reconstructBoard(boardStateElems):
    b = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
    for i in range(3):
        rowElements = boardStateElems[i].split(',')
        for j, val in enumerate(rowElements):
            if j == 0:
                # Get rid of opening brace if it's first element
                # print(val.split('['))
                val = val.split('[')[1]
            elif j == 2:
                # Get rid of closing brance if it's last element
                # print(val.split(']'))
                val = val.split(']')[0]
            b[i][j] = int(val.strip())
    return b


def trainTeacher(dojoFilePath):
    nLosses = 0
    nWins = 0
    nTies = 0
    nGames = 0

    gameTrace = []
    iGameTrace = []
    if expressivity == 'compact':
        weights = [0.1, 0.1, 0.1, 0.1, 0.1]
    elif expressivity == 'full':
        weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                   0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    # weights = [0.1, 0.1, 0.1, 0.1, 0.1]

    with open(dojoFilePath) as dojo:
        boardStates = dojo.readlines()
        for i, boardState in enumerate(boardStates):
            stateElements = boardState.split(';')
            for j in range(len(stateElements)):
                # Strip of white space and newline
                stateElements[j] = stateElements[j].strip()
            if stateElements[-1] != '':
                b = reconstructBoard(stateElements)
                gameTrace.append(b)  # Append final state
                iGameTrace.append(board_utils.invertBoard(b))
                nGames += 2
                # print('State is Final state')
                if int(stateElements[-1]) == 1:
                    if verbose:
                        print('Computer won!')
                    nWins += 1
                    nLosses += 1  # Account for inverted games
                    # Train on gameTrace
                elif int(stateElements[-1]) == -1:
                    if verbose:
                        print('Computer lost!')
                    nLosses += 1
                    nWins += 1  # Account for inverted games
                    # Train on gameTrace
                elif int(stateElements[-1]) == 0:
                    if verbose:
                        print('Tie!')
                    nTies += 2
                # Get training examples from gameTrace
                boardStates, v_trains = critic.getTrainingExamples(
                    gameTrace, weights, expressivity)

                iBoardStates, iv_trains = critic.getTrainingExamples(
                    iGameTrace, weights, expressivity)
                # train
                if expressivity == 'compact':
                    weights, error = generalizer.LMSWeightUpdate(
                        weights, boardStates, v_trains, lr=lr)
                    # Train on inverted games
                    weights, error = generalizer.LMSWeightUpdate(
                        weights, iBoardStates, iv_trains, lr=lr)
                elif expressivity == 'full':
                    weights, error = generalizer.LMSWeightUpdateFull(
                        weights, boardStates, v_trains, lr=lr)
                    # Train on inverted games
                    weights, error = generalizer.LMSWeightUpdateFull(
                        weights, iBoardStates, iv_trains, lr=lr)
                if verbose:
                    print(f'New weights: {weights}')
                gameTrace = []  # Reset GameTrace for next game in dojo
                igameTrace = []

            else:
                # This is a regular board state convert to 2d list and append to gameTrace
                b = reconstructBoard(stateElements)
                gameTrace.append(b)
                iGameTrace.append(board_utils.invertBoard(b))
                if verbose:
                    board_utils.drawBoard(b)

    print(f'Trained on {nGames} games')
    return weights, [nWins/nGames, nLosses/nGames, nTies/nGames]


if __name__ == '__main__':
    if os.path.getsize(DOJO_FILE_PATH) == 0:
        print('[ERROR] Training file is empty')
        sys.exit()
    if len(sys.argv) == 1:
        print('[ERROR] You need expressivity argument')
        print('Example: \n"python3 testTeacher.py compact" for compact expressivity')
        print('"python3 testTeacher.py full" for full expressivity')
        print('compact is preferred')
        sys.exit()
    for i, arg in enumerate(sys.argv):
        if i == 1:
            expressivity = arg  # First arg is expressivity
        # print(f"Argument {i:>6}: {arg}")
    print(f'Expressivity: {expressivity}')
    print('Training...')
    weights, stats = trainTeacher(DOJO_FILE_PATH)
    print('Done!')
    print(f'Weights after training: {weights}')
    print(f'============= Victories {stats[0]*100} % ==============')
    print(
        f'=============   Losses  {stats[1]*100} % ==============')
    print(f'=============    Ties   {stats[2]*100} % ==============')

    # Test: (Play human opponent)
    play_utils.test(weights, expressivity)
