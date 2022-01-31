from board_utils import BoardUtils

board_utils = BoardUtils()


class Critic:
    def __init__(self):
        self.w = []

    # def getTrainingExamples(self, gameTrace, w):
    #     self.w = w
    #     size = len(gameTrace)
    #     v_trains = []
    #     for i in range(size):
    #         b = gameHistory[size-1]  # Final board state
    #         v_train = self.getFinalScore(b)

    def getTrainingExamples(self, gameTrace, w):
        v_trains = []
        systemGameTrace = []
        # print(gameTrace)
        gameTrace.reverse()
        # print(gameTrace)
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
                v_trains.append(self.v_hat(gameTrace[i-1]))
                systemGameTrace.append(b)

        del gameTrace
        # Reverse again to get correct order
        systemGameTrace.reverse()
        v_trains.reverse()

        return systemGameTrace, v_trains

    def getFinalScore(self, b):
        # Won, Lost on Tie?
        # The game may not be completely done. You need to detect about to (situations) (disregard this, may be true if I go firt instead of opponent)
        if board_utils.gameWon(b, 1):
            print('Won!')
            v_train = 1
        elif board_utils.gameWon(b, -1):
            print('Lost.')
            v_train = -1
        elif board_utils.gameTie(b):
            print('Tie.')
            v_train = 0
        print('Final board state')
        board_utils.drawBoard(b)
        return v_train

    def v_hat(self, b):
        return board_utils.evaluateBoardState(b, self.w, expressivity='compact')
