from board_utils import BoardUtils
import random

board_utils = BoardUtils()


class PerfSystem:
    def __init__(self):
        self.data = []
        self.w = []
        self.verbose = False
        # self.board_utils = BoardUtils()

    def setVerbose(self, verbose):
        self.verbose = verbose

    def play(self, b, w, expressivity):
        # Calculate v_hat
        # Extract fetures from the board (x1, x2, x3 ,x4)
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
        # x1, x2, min_x_to_v, min_o_to_v = board_utils.getStateFeatures(
        #     b, expressivity=expressivity)
        # print(f'x1: {x1}')
        # print(f'x2: {x2}')
        # print(f'min_x_to_v: {min_x_to_v}')
        # print(f'min_o_to_v: {min_o_to_v}')
        # self.w = w
        # if expressivity == 'compact':
        #     v_hat = self.w[0] + self.w[1]*x1 + self.w[2]*x2 + \
        #         self.w[3]*min_x_to_v + self.w[4]*min_o_to_v
        #     # ChooseMove that will maximize v_hat
        # self.chooseMove(b)

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
        # print(f'Moves = {moves}')
        # Apply the moves in a loop and recalculate v_hat to see which one maximizes it
        v_temps = []
        for m in moves:
            b[m[0]][m[1]] = 1
            # board_utils.drawBoard(b)
            v_temp = board_utils.evaluateBoardState(
                b, self.w, self.expressivity)
            v_temps.append(v_temp)
            # print(f'move = {m}, v_hat(b) = {v_temp}')
            b[m[0]][m[1]] = 0  # Undo the move
            # print('----------------------------')
        if self.verbose:
            print(f'{moves}')
            print(f'v_temps = {v_temps}')
        optimalMove = moves[v_temps.index(max(v_temps))]
        if self.verbose:
            print(f'Best move = {optimalMove}')
        return optimalMove
