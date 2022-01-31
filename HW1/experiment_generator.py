# import numpy as np
import random
from perf_system import PerfSystem
from board_utils import BoardUtils
# import logging

# logging.basicConfig()

board_utils = BoardUtils()
perf_system = PerfSystem()


class ExperimentGenerator:
    def __init__(self, random_prob, go_first_prob):
        self.data = []
        self.random_prob = random_prob
        self.go_first_prob = go_first_prob
        self.TAG = 'EXP_GEN: '
    # Input, currently learned function v_hat (May not be required when generating random states)
    # Output, board state fro a new game
    # Generate random board states 80% of the time, 20% of the time pickup a state from a lost game using a queue.

    def generateBoard(self, weights, opponent):
        p = random.uniform(0.0, 1.0)
        print(p)
        iGoFirst = False
        # if queues of lost games is not empty
        if p > (1 - self.random_prob):
            # logging.info(self.TAG + "Generating random board state")
            print(self.TAG + "Generating new board state")
            # Gen random state
            # 3x3 matrix, generate random int tuple to indicate a cell.
            # sx = random.randint(0, 2)
            # sy = random.randint(0, 2)
            b = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]

            # b = np.zeros((3, 3))
            # Going first with probability go_first_prob
            if random.uniform(0.0, 1.0) > (1-self.go_first_prob):
                print('Going first!')
                # b[sx][sy] = 1
                b = perf_system.play(b, weights, expressivity='compact')
                iGoFirst = True
            else:
                if opponent == 'random':
                    # b[sx][sy] = -1
                    ob = board_utils.invertBoard(b)
                    ob = perf_system.chooseRandomMove(ob)
                    b = board_utils.invertBoard(ob)
                elif opponent == 'ai':
                    ob = board_utils.invertBoard(b)
                    ob = perf_system.play(
                        ob, weights, expressivity='compact')
                    b = board_utils.invertBoard(ob)

            return b, iGoFirst
        else:
            # logging.info(self.TAG + "Picking state from lost game")
            print(self.TAG + "Picking state from lost game")
            print("Picking state from lost game")
            # TODO: Get queues of lost games from main and output them here
            # Pick state from previous lost game
