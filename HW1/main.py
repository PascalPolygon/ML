# import sys
# import logging
from experiment_generator import ExperimentGenerator
from board_utils import BoardUtils
from perf_system import PerfSystem
from critic import Critic
from generalizer import Generalizer
import random
# import matplotlib.pyplot as plt

# logging.basicConfig(level=logging.INFO)
# logging.info('Hello world!')
# logging.basicConfig(level=logging.NOTSET)
# logger = logging.getLogger('main')


def main():
    exp_gen = ExperimentGenerator(1.0)
    board_utils = BoardUtils()
    perf_system = PerfSystem()
    critic = Critic()
    generalizer = Generalizer()
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

    weights = [0.1, 0.1, 0.1, 0.1, 0.1]
    for rnd in range(20):
        print('==================================================')
        if rnd > 0:
            vics = wins/rnd
            victories.append(vics)
            print(f'===================== ROUND {rnd} =======================')
            print(f'============= Victories {vics*100} % ==============')
            print(
                f'=============   Losses  {(losses/rnd)*100} % ==============')
            print(f'=============    Ties   {(ties/rnd)*100} % ==============')

        print('==================================================')
        ai_opponent_percentage = 0.8
        # Determine if opponent is AI or random mover with some probability
        # if np.random.uniform(0.0, 1.0) > ai_opponent_percentage:
        if random.uniform(0.0, 1.0) > ai_opponent_percentage:
            # Play AI (self)
            opponent = 'ai'
        else:
            # Play random mover
            opponent = 'random'

        # opponent = 'ai'  # Only play self
        # opponent = 'random'  # Only play random
        # weights = [0.1, 0.1, 0.1, 0.1, 0.1]
        b = exp_gen.generateBoard(weights)
        board_utils.drawBoard(b)
        print(f'Old weights: {weights}')
        f = board_utils.getStateFeatures(b, expressivity='compact')
        if b is not None:
            gameTrace = []
            while(not board_utils.isFinalState(b)):
                print('ego')
                b = perf_system.play(b, weights, expressivity='compact')
                gameTrace.append(b)
                if board_utils.isFinalState(b):
                    break  # Exit the game loop
                # opponent = 'ai'
                if opponent == 'ai':
                    # Replace X's w O's (and vice-versa) and let perf_system play again
                    ob = board_utils.invertBoard(b)
                    ob = perf_system.play(ob, weights, expressivity='compact')
                    b = board_utils.invertBoard(ob)
                elif opponent == 'random':
                    ob = board_utils.invertBoard(b)
                    ob = perf_system.chooseRandomMove(ob)
                    b = board_utils.invertBoard(ob)

                print('==================================================')

            print('Game ended')
            print('==================================================')
            board_utils.drawBoard(b)
            boardStates, v_trains = critic.getTrainingExamples(
                gameTrace, weights)
            print('Training examples')
            print('==================================================')

            # Update weights w Generalizer
            weights, error = generalizer.LMSWeightUpdate(
                weights, boardStates, v_trains, lr=0.01)
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

    print('ERRORS')
    print(errors)
    print('Victories %')
    print(victories)
    # plt.plot(victories)
    # plt.title(f'Victores % {ai_opponent_percentage*100}% sefl play')
    # plt.show()
    print(f'Mean Won Errors ({len(wonErrors)})')
    # print(np.mean(wonErrors))
    print(wonErrors)
    # plt.plot(wonErrors)
    # plt.title(
    #     f'LMS error on won games {ai_opponent_percentage*100}% sefl play')
    # plt.show()

    print(f'LMS error on tied games ({len(tieErrors)})')
    print(tieErrors)
    # plt.plot(tieErrors)
    # plt.title(f'LMS tied on won games {ai_opponent_percentage*100}% sefl play')
    # plt.show()

    print(f'LMS error on lost games ({len(lostErrors)})')
    # print(np.mean(lostErrors))
    print(lostErrors)
    # plt.plot(lostErrors)
    # plt.title(
    #     f'LMS tied on lost games {ai_opponent_percentage*100}% sefl play')
    # plt.show()

    # print('Last board in gameTrace')
    # print('==================================================')
    # board_utils.drawBoard(gameTrace[-1])

    # print(b)
    # logger.info(b)


if __name__ == '__main__':
    # logger.info('Hello world!')
    # print('Hello world!')

    main()
    # sys.exit(main())
