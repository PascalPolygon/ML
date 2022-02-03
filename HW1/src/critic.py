from board_utils import BoardUtils

board_utils = BoardUtils()


class Critic:
    def __init__(self):
        self.w = []
        self.verbose = False

    def getTrainingExamples(self, gameTrace, w, expressivity):
        v_trains = []
        systemGameTrace = []
        gameTrace.reverse()
        self.w = w
        for i, b in enumerate(gameTrace):
            # Starting w final state because we reversed the gameTrace
            if i == 0:
                # This is the appended final state
                v_train_final = self.getFinalScore(b)
            # Second to last (Actual last board from perf system's perspective)
            elif i == 1:
                v_trains.append(v_train_final)
                systemGameTrace.append(b)
            else:
                # v_trains = v_hat(successor(b)) but we will use v_hat(predessor(b)) becaue we reversed the gameTrace
                v_trains.append(self.v_hat(gameTrace[i-1], expressivity))
                systemGameTrace.append(b)

        del gameTrace
        # Reverse again to get correct order
        systemGameTrace.reverse()
        v_trains.reverse()

        return systemGameTrace, v_trains

    def getFinalScore(self, b):
        # Won, Lost on Tie?
        if self.verbose:
            print('getFinalScore of:')
            board_utils.drawBoard(b)
        if board_utils.gameWon(b, 1):
            if self.verbose:
                print('Won!')
            v_train = 1
        elif board_utils.gameWon(b, -1):
            if self.verbose:
                print('Lost.')
            v_train = -1
        elif board_utils.gameTie(b):
            if self.verbose:
                print('Tie.')
            v_train = 0
        if self.verbose:
            print('Final board state')
            board_utils.drawBoard(b)
        return v_train

    def v_hat(self, b, expressivity):
        return board_utils.evaluateBoardState(b, self.w, expressivity)
