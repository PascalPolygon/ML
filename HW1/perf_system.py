from board_utils import BoardUtils
import numpy as np

board_utils = BoardUtils()


class PerfSystem:
    def __init__(self):
        self.data = []
        # self.board_utils = BoardUtils()

    def play(self, b, weights):
        # Calculate v_hat
        # Extract fetures from the board (x1, x2, x3 ,x4)
        [x1, x2] = board_utils.getStateFeatures(b)
