# import sys
# import logging
from experiment_generator import ExperimentGenerator
from board_utils import BoardUtils
from perf_system import PerfSystem
from critic import Critic
from generalizer import Generalizer
import numpy as np

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

    weights = [0.1, 0.1, 0.1, 0.1, 0.1]
    for rnd in range(50):
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
    # Determine if opponent is AI or random mover with some probability
        if np.random.uniform(0.0, 1.0) > 0.3:
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
        # print(b)
        if b is not None:
            gameTrace = []
            while(not board_utils.isFinalState(b)):
                # board_utils.drawBoard(b)
                print('ego')
                b = perf_system.play(b, weights, expressivity='compact')
                # board_utils.drawBoard(b)
                gameTrace.append(b)
                # opponent = 'ai'
                if opponent == 'ai':
                    # Replace X's w O's (and vice-versa) and let perf_system play again
                    ob = board_utils.invertBoard(b)
                    # print('Playing peer')
                    # print(f'Opponent')
                    ob = perf_system.play(ob, weights, expressivity='compact')
                    b = board_utils.invertBoard(ob)
                    board_utils.drawBoard(b)
                elif opponent == 'random':
                    ob = board_utils.invertBoard(b)
                    ob = perf_system.chooseRandomMove(ob)
                    b = board_utils.invertBoard(ob)
                    # board_utils.drawBoard(b)

                print('==================================================')

            print('Game ended')
            print('==================================================')
            board_utils.drawBoard(b)
            if (board_utils.gameWon(b, 1)):
                wins += 1
            elif (board_utils.gameWon(b, -1)):
                losses += 1
            elif (board_utils.gameTie(b)):
                ties += 1
            # Send game history to citic to genrate training examples
            boardStates, v_trains = critic.getTrainingExamples(
                gameTrace, weights)
            print('Training examples')
            print('==================================================')
            board_utils.drawBoard(boardStates[-1])
            # print(v_trains)
            # Update weights w Generalizer
            weights, error = generalizer.LMSWeightUpdate(
                weights, boardStates, v_trains, lr=0.01)
            print(f'New weights: {weights}')
            errors.append(error)
        # if board_utils.gameWon(b, 1):
        #     print('Won!')
        #     v_train = 100
        # elif board_utils.gameWon(b, -1):
        #     print('Lost.')
        #     v_train = -100
        # elif board_utils.gameTie(b):
        #     print('Tie.')
        #     v_train = 0
    print('ERRORS')
    print(errors)
    print('Victories %')
    print(victories)
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
