from board_utils import BoardUtils
import random

board_utils = BoardUtils()


class PerfSystem:
    def __init__(self):
        self.data = []
        self.w = []
        self.verbose = False

    def setVerbose(self, verbose):
        self.verbose = verbose

    def play(self, b, w, expressivity):
        self.w = w
        self.expressivity = expressivity
        v_hat = board_utils.evaluateBoardState(b, self.w, self.expressivity)
        if self.verbose:
            print(f'V_hat = {v_hat}')
        move = self.chooseMove(b)
        # Execute move
        b[move[0]][move[1]] = 1
        v_hat = board_utils.evaluateBoardState(b, self.w, self.expressivity)
        if self.verbose:
            print(f'New V_hat = {v_hat}')
        return b

    def chooseRandomMove(self, b):
        moves = board_utils.getLegalMoves(b)
        rm = random.randint(0, len(moves)-1)
        if self.verbose:
            print(f'random move id: {rm}')
        b[moves[rm][0]][moves[rm][1]] = 1
        return b

    def chooseMove(self, b):
        # Get a list of possible moves (Evaluate board to see what are all the current possible legal moves)
        moves = board_utils.getLegalMoves(b)
        # Apply the moves in a loop and recalculate v_hat to see which one maximizes it
        v_temps = []
        for m in moves:
            b[m[0]][m[1]] = 1
            v_temp = board_utils.evaluateBoardState(
                b, self.w, self.expressivity)
            v_temps.append(v_temp)
            b[m[0]][m[1]] = 0  # Undo the move
        if self.verbose:
            print(f'{moves}')
            print(f'v_temps = {v_temps}')
        optimalMove = moves[v_temps.index(max(v_temps))]
        if self.verbose:
            print(f'Best move = {optimalMove}')
        return optimalMove
