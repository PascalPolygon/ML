# import sys
# import logging
from experiment_generator import ExperimentGenerator
from board_utils import BoardUtils
from perf_system import PerfSystem
from critic import Critic
import numpy as np

# logging.basicConfig(level=logging.INFO)
# logging.info('Hello world!')
# logging.basicConfig(level=logging.NOTSET)
# logger = logging.getLogger('main')


def main():
    exp_gen = ExperimentGenerator(0.8)
    board_utils = BoardUtils()
    perf_system = PerfSystem()
    critic = Critic()

    # Determine if opponent is AI or random mover with some probability
    # p = np.random.uniform(0.0, 1.0)
    # print(p)
    # if queues of lost games is not empty
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
                print('Playing peer')
                print(f'Opponent')
                # board_utils.drawBoard(ob)
                ob = perf_system.play(ob, weights, expressivity='compact')
                # board_utils.drawBoard(ob)
                b = board_utils.invertBoard(ob)
                board_utils.drawBoard(b)
                # gameHistory.append(b)
            elif opponent == 'random':
                ob = board_utils.invertBoard(b)
                print('Playing random')
                print(f'Opponent')
                # board_utils.drawBoard(ob)
                # ob = perf_system.play(ob, weights, expressivity='compact')
                ob = perf_system.chooseRandomMove(ob)
                # board_utils.drawBoard(ob)
                b = board_utils.invertBoard(ob)
                board_utils.drawBoard(b)
                # gameHistory.append(b)

            print('==================================================')

        print('Game ended')
        print('==================================================')
        board_utils.drawBoard(b)
        # Send game history to citic to genrate training examples
        boardStates, v_trains = critic.getTrainingExamples(gameTrace, weights)
        print('Training examples')
        print('==================================================')
        board_utils.drawBoard(boardStates[-1])
        print(v_trains)
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
