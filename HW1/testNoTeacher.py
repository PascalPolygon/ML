# import sys
# import logging
from experiment_generator import ExperimentGenerator
from board_utils import BoardUtils
from perf_system import PerfSystem
from critic import Critic
from generalizer import Generalizer
import random
import matplotlib.pyplot as plt
import sys
import os
from play_utils import PlayUtils

# logging.basicConfig(level=logging.INFO)
# logging.info('Hello world!')
# logging.basicConfig(level=logging.NOTSET)
# logger = logging.getLogger('main')
exp_gen = ExperimentGenerator(1.0, 0.5)
board_utils = BoardUtils()
perf_system = PerfSystem()
critic = Critic()
generalizer = Generalizer()


TRAINING_FILE_PATH = os.getcwd()+'/dojo.txt'
play_utils = PlayUtils(TRAINING_FILE_PATH)


def trainNoTeacher(maxEpochs, ai_opponent_percentage, lr, expressivity, verbose=True):

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

    if expressivity == 'compact':
        weights = [0.1, 0.1, 0.1, 0.1, 0.1]
    elif expressivity == 'full':
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
        b, iGoFirst = exp_gen.generateBoard(weights, opponent, expressivity)
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
                        # ob = perf_system.play(
                        #     ob, weights, expressivity='full')
                        ob = perf_system.play(
                            ob, weights, expressivity)
                        b = board_utils.invertBoard(ob)
                    elif opponent == 'random':
                        ob = board_utils.invertBoard(b)
                        ob = perf_system.chooseRandomMove(ob)
                        b = board_utils.invertBoard(ob)
                    continue

                if verbose:
                    print('ego')
                # b = perf_system.play(b, weights, expressivity='compact')
                b = perf_system.play(b, weights, expressivity)
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
                    ob = perf_system.play(
                        ob, weights, expressivity)
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
                if expressivity == 'compact':
                    print(
                        f"Final board features(compact) {board_utils.getStateFeatures(b, expressivity)}")
                elif expressivity == 'full':
                    print(
                        f"Final board features(full) {board_utils.getStateFeatures(b, expressivity)}")
            boardStates, v_trains = critic.getTrainingExamples(
                gameTrace, weights, expressivity)
            if verbose:
                print('Training examples')
                print('==================================================')

            # Update weights w Generalizer
            if expressivity == 'compact':
                weights, error = generalizer.LMSWeightUpdate(
                    weights, boardStates, v_trains, lr=lr)
            elif expressivity == 'full':
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
    # dojoFile.close()


def main(expressivty):
    maxEpochs = 300
    lr = 0.001  # Higher lr will win more agains self but also ties less
    selfPlay = 0.9
    # expressivity = 'compact'
    # expressivity = 'full'
    print('Training...')
    weights, stats = trainNoTeacher(
        maxEpochs, selfPlay, lr, expressivity, verbose=False)
    print('Done!')
    print(f'Weights after training: {weights}')
    print(f'============= Victories {stats[0]*100} % ==============')
    print(
        f'=============   Losses  {stats[1]*100} % ==============')
    print(f'=============    Ties   {stats[2]*100} % ==============')

    # Test: (Play human opponent)
    play_utils.test(weights, expressivity)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('[ERROR] You need expressivity argument')
        print('Example: \n"python3 testNoTeacher.py compact" for compact expressivity')
        print('"python3 testNoTeacher.py full" for full expressivity')
        print('compact is preferred')
        sys.exit()
    for i, arg in enumerate(sys.argv):
        if i == 1:
            expressivity = arg  # First arg is expressivity
        # print(f"Argument {i:>6}: {arg}")
    print(f'Expressivity: {expressivity}')
    main(expressivity)
    # sys.exit(main())
