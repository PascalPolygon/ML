import numpy as np
import random
# import logging

# logging.basicConfig()


class ExperimentGenerator:
    def __init__(self, random_prob):
        self.data = []
        self.random_prob = random_prob
        self.TAG = 'EXP_GEN: '
    # Input, currently learned function v_hat (May not be required when generating random states)
    # Output, board state fro a new game
    # Generate random board states 80% of the time, 20% of the time pickup a state from a lost game using a queue.

    def generateBoard(self, weights):
        p = np.random.uniform(0.0, 1.0)
        print(p)
        # if queues of lost games is not empty
        if p > (1 - self.random_prob):
            # logging.info(self.TAG + "Generating random board state")
            print(self.TAG + "Generating random board state")
            # Gen random state
            # 3x3 matrix, generate random int tuple to indicate a cell.
            sx = random.randint(0, 2)
            sy = random.randint(0, 2)
            b = np.zeros((3, 3))
            b[sx][sy] = -1
            return b
        else:
            # logging.info(self.TAG + "Picking state from lost game")
            print(self.TAG + "Picking state from lost game")
            print("Picking state from lost game")
            # Pick state from previous lost game
