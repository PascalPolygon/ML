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
        self.verbose = False

    def generateBoard(self, weights, opponent, expressivity):
        p = random.uniform(0.0, 1.0)
        # print(p)
        iGoFirst = False

        if p > (1 - self.random_prob):
            if (self.verbose):
                print(self.TAG + "Generating new board state")
            b = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]

            if random.uniform(0.0, 1.0) > (1-self.go_first_prob):
                if self.verbose:
                    print(self.TAG + "Going first!")

                b = perf_system.chooseRandomMove(b)
                iGoFirst = True
            else:
                if opponent == 'random':
                    ob = board_utils.invertBoard(b)
                    ob = perf_system.chooseRandomMove(ob)
                    b = board_utils.invertBoard(ob)
                elif opponent == 'ai':
                    ob = board_utils.invertBoard(b)
                    ob = perf_system.play(
                        ob, weights, expressivity)
                    b = board_utils.invertBoard(ob)

            return b, iGoFirst
        else:
            # Pick state from previously lost game as starting board state (Not implemented here)
            if self.verbose:
                print(self.TAG + "Picking state from lost game")
                print("Picking state from lost game [NOT IMPLEMENTED")
            # TODO: Get queues of lost games from main and output them here
            # Pick state from previous lost game
