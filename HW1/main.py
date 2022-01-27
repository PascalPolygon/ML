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

    for rnd in range(4):
        print('==================================================')
        if rnd > 0:
            print(f'======== ROUND {rnd}: {(wins/rnd)*100}% victories =======')
        print('==================================================')
    # Determine if opponent is AI or random mover with some probability
        if np.random.uniform(0.0, 1.0) > 0.5:
            # Play AI (self)
            opponent = 'ai'
        else:
            # Play random mover
            opponent = 'random'

        weights = [0.1, 0.1, 0.1, 0.1, 0.1]
        b = exp_gen.generateBoard(weights)
        # print(b)
        if b is not None:
            gameTrace = []
            while(not board_utils.isFinalState(b)):
                # board_utils.drawBoard(b)
                print('ego')
                b = perf_system.play(b, weights, expressivity='compact')
                board_utils.drawBoard(b)
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
            # Send game history to citic to genrate training examples
            boardStates, v_trains = critic.getTrainingExamples(
                gameTrace, weights)
            print('Training examples')
            print('==================================================')
            board_utils.drawBoard(boardStates[-1])
            # print(v_trains)
            # Update weights w Generalizer
            weights = generalizer.LMSWeightUpdate(
                weights, boardStates, v_trains)
            print(f'New weights: {weights}')
        # if board_utils.gameWon(b, 1):
        #     print('Won!')
        #     v_train = 100
        # elif board_utils.gameWon(b, -1):
        #     print('Lost.')
        #     v_train = -100
        # elif board_utils.gameTie(b):
        #     print('Tie.')
        #     v_train = 0

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
