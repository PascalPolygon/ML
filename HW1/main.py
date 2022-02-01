# import sys
# import logging
from experiment_generator import ExperimentGenerator
from board_utils import BoardUtils
from perf_system import PerfSystem
from critic import Critic
from generalizer import Generalizer
import random
import matplotlib.pyplot as plt

# logging.basicConfig(level=logging.INFO)
# logging.info('Hello world!')
# logging.basicConfig(level=logging.NOTSET)
# logger = logging.getLogger('main')
exp_gen = ExperimentGenerator(1.0, 0.5)
board_utils = BoardUtils()
perf_system = PerfSystem()
critic = Critic()
generalizer = Generalizer()


def trainNoTeacher(maxEpochs, ai_opponent_percentage, lr, verbose=True):

    wins = 0
    losses = 0
    ties = 0
    errors = []
    victories = []
    tieErrors = []
    wonErrors = []
    lostErrors = []

    # TODO: Make into a Queue
    lostGames = []
    lostV_trains = []

    perf_system.setVerbose(verbose)
    generalizer.verbose = False
    critic.verbose = False

    # weights = [0.1, 0.1, 0.1, 0.1, 0.1]
    weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
               0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    for rnd in range(maxEpochs):
        if verbose:
            print('==================================================')
        if rnd > 0:
            vics = wins/rnd
            los = losses/rnd
            ts = ties/rnd
            victories.append(vics)
            if verbose:
                print(
                    f'===================== ROUND {rnd} =======================')
                print(f'============= Victories {vics*100} % ==============')
                print(
                    f'=============   Losses  {(los)*100} % ==============')
                print(f'=============    Ties   {(ts)*100} % ==============')

        if verbose:
            print('==================================================')
        # ai_opponent_percentage = selfPlayP
        # Determine if opponent is AI or random mover with some probability
        # if np.random.uniform(0.0, 1.0) > ai_opponent_percentage:
        if random.uniform(0.0, 1.0) > (1 - ai_opponent_percentage):
            # Play AI (self)
            opponent = 'ai'
        else:
            # Play random mover
            opponent = 'random'

        # opponent = 'ai'  # Only play self
        # opponent = 'random'  # Only play random
        # weights = [0.1, 0.1, 0.1, 0.1, 0.1]
        b, iGoFirst = exp_gen.generateBoard(weights, opponent)
        if verbose:
            board_utils.drawBoard(b)
            print(f'Old weights: {weights}')
        # f = board_utils.getStateFeatures(b, expressivity='compact')
        if b is not None:
            gameTrace = []
            while(not board_utils.isFinalState(b)):
                # if not iGoFirst:
                if iGoFirst:
                    iGoFirst = False
                    if opponent == 'ai':  # Let opponent play since I went first
                        # Replace X's w O's (and vice-versa) and let perf_system play again
                        ob = board_utils.invertBoard(b)
                        # ob = perf_system.play(
                        #     ob, weights, expressivity='compact')
                        ob = perf_system.play(
                            ob, weights, expressivity='full')
                        b = board_utils.invertBoard(ob)
                    elif opponent == 'random':
                        ob = board_utils.invertBoard(b)
                        ob = perf_system.chooseRandomMove(ob)
                        b = board_utils.invertBoard(ob)
                    continue

                if verbose:
                    print('ego')
                # b = perf_system.play(b, weights, expressivity='compact')
                b = perf_system.play(b, weights, expressivity='full')
                gameTrace.append(b)
                if board_utils.isFinalState(b):
                    if verbose:
                        print('Final sate from loop')
                    break  # Exit the game loop
                # opponent = 'ai'
                if opponent == 'ai':
                    # Replace X's w O's (and vice-versa) and let perf_system play again
                    ob = board_utils.invertBoard(b)
                    # ob = perf_system.play(ob, weights, expressivity='compact')
                    ob = perf_system.play(ob, weights, expressivity='full')
                    b = board_utils.invertBoard(ob)
                elif opponent == 'random':
                    ob = board_utils.invertBoard(b)
                    ob = perf_system.chooseRandomMove(ob)
                    b = board_utils.invertBoard(ob)

                if verbose:
                    print('==================================================')

            if verbose:
                print('Game ended')
                print('==================================================')
                board_utils.drawBoard(b)
            # Append the final board state to get the v_hat of final state. This v_hat is the same as second to last
            gameTrace.append(b)
            # print(
            #     f"Final board features {board_utils.getStateFeatures(b, expressivity='full')}")
            if verbose:
                # print(
                #     f"Final board features(compact) {board_utils.getStateFeatures(b, expressivity='compact')}")
                print(
                    f"Final board features(full) {board_utils.getStateFeatures(b, expressivity='full')}")
            boardStates, v_trains = critic.getTrainingExamples(
                gameTrace, weights)
            if verbose:
                print('Training examples')
                print('==================================================')

            # Update weights w Generalizer
            # weights, error = generalizer.LMSWeightUpdate(
            #     weights, boardStates, v_trains, lr=lr)
            weights, error = generalizer.LMSWeightUpdateFull(
                weights, boardStates, v_trains, lr=lr)
            if verbose:
                print(f'New weights: {weights}')
            errors.append(error)

            if (board_utils.gameTie(b)):
                # tie
                tieErrors.append(error)
                ties += 1
            elif (board_utils.gameWon(b, 1)):
                wonErrors.append(error)
                wins += 1
            elif (board_utils.gameWon(b, -1)):
                lostErrors.append(error)
                losses += 1
                # Add to list of lost games
                # TODO: Make into a queue
                lostGames.append(boardStates)
                lostV_trains.append(v_trains)

    # print('ERRORS')
    # print(errors)
    # print('Victories %')
    # print(victories)
    plt.plot(victories)
    plt.title(f'Victores % {ai_opponent_percentage*100}% sefl play')
    plt.show()
    # print(f'LMS error on won Errors ({len(wonErrors)})')
    # print(wonErrors)
    plt.plot(wonErrors)
    plt.title(
        f'LMS error on won games {ai_opponent_percentage*100}% sefl play')
    plt.show()

    # # print(f'LMS error on tied games ({len(tieErrors)})')
    plt.plot(tieErrors)
    plt.title(
        f'LMS tied on tied games {ai_opponent_percentage*100}% sefl play')
    plt.show()

    # # print(f'LMS error on lost games ({len(lostErrors)})')
    # # # print(np.mean(lostErrors))
    # # # print(lostErrors)
    # plt.plot(lostErrors)
    # plt.title(
    #     f'LMS tied on lost games {ai_opponent_percentage*100}% sefl play')
    # plt.show()
    return weights, [vics, los, ts]


def getPlayerMove():
    print('Enter your move, use row (0-2) and column (0-2) numbers')
    r = input("row number: ")
    c = input('col number: ')
    try:
        r = int(r)
        c = int(c)
    except ValueError:
        print('**[ERROR] Input must an integer')
        return None

    if r < 0 or r > 2 or c < 0 or c > 2:
        print('**[ERROR] You can only use numbers: (0,1,2)')
        return None
        # continue
    print(f'Your move = [{r} {c}]')
    return r, c


def gameOver(b):
    if (board_utils.isFinalState(b)):
        if (board_utils.gameWon(b, 1)):
            print('Computer win!')
        elif (board_utils.gameWon(b, -1)):
            print('You win')
        return True
    else:
        return False


def playerMove(b):
    move = getPlayerMove()
    if move is None:
        return False
    else:
        r, c = move
        b[r][c] = -1
        board_utils.drawBoard(b)
        return b


def computerMove(b, weights):
    print('Computer move:')
    # b = perf_system.play(b, weights, expressivity='compact')
    b = perf_system.play(b, weights, expressivity='full')
    board_utils.drawBoard(b)
    return b


def test(weights):
    gameOn = True
    while gameOn:
        a = ''
        a = input("Hello human, do you want to go first? (y/n), q to quit: ")
        b = [[0, 0, 0],  # init board
             [0, 0, 0],
             [0, 0, 0]]
        if a == 'y' or a == 'Y':
            # print(a)
            print('Ok, you go first!')
            board_utils.drawBoard(b)
            # Input rows and cols to play and drawboard
            gameOn = True
            # while gameOn:
            while(not board_utils.isFinalState(b)):
                nb = playerMove(b)
                while not nb:
                    nb = playerMove(b)
                b = nb
                if gameOver(b):
                    break
                # COmputer move
                b = computerMove(b, weights)
                print('------------------------------------------')
            gameOver(b)
        elif a == 'n' or a == 'N':
            print('Ok, I go first!')
            # perf_sytem makes first move and drawboard
            gameOn = True
            while(not board_utils.isFinalState(b)):
                if board_utils.isEmpty(b):
                    # Random move to start the game
                    b = perf_system.chooseRandomMove(b)
                    board_utils.drawBoard(b)
                else:
                    b = computerMove(b, weights)

                if gameOver(b):
                    break
                nb = playerMove(b)
                while not nb:
                    nb = playerMove(b)
                b = nb

                print('------------------------------------------')
            gameOver(b)
        elif a == 'q' or a == 'Q':
            print('Bye-bye!')
            gameOn = False


def main():
    maxEpochs = 30000
    lr = 0.001  # Higher lr will win more agains self but also ties less
    selfPlay = 0.9
    print('Training...')
    weights, stats = trainNoTeacher(maxEpochs, selfPlay, lr, verbose=False)
    print('Done!')
    print(f'Weights after training: {weights}')
    print(f'============= Victories {stats[0]} % ==============')
    print(
        f'=============   Losses  {stats[1]} % ==============')
    print(f'=============    Ties   {stats[2]} % ==============')

    # Test: (Play human opponent)
    test(weights)


if __name__ == '__main__':
    # logger.info('Hello world!')
    # print('Hello world!')
    main()
    # sys.exit(main())
