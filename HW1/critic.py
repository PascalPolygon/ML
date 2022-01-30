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
        # print(gameTrace)
        gameTrace.reverse()
        # print(gameTrace)
        self.w = w
        for i, b in enumerate(gameTrace):
            # Starting w final state because we reversed the gameTrace
            if i == 0:
                # This is the final state
                v_trains.append(self.getFinalScore(b))
            else:
                # v_trains = v_hat(successor(b)) but we will use v_hat(predessor(b)) becaue we reversed the gameTrace
                v_trains.append(self.v_hat(gameTrace[i-1]))
         # Reverse again to get correct order
        gameTrace.reverse()
        v_trains.reverse()

        return gameTrace, v_trains

    def getFinalScore(self, b):
        # Won, Lost on Tie?
        # The game may not be completely done. You need to detect about to (situations) (disregard this, may be true if I go firt instead of opponent)
        if board_utils.gameWon(b, 1):
            print('Won!')
            v_train = 10
        elif board_utils.gameWon(b, -1):
            print('Lost.')
            v_train = -10
        elif board_utils.gameTie(b):
            print('Tie.')
            v_train = 0
        print('Final board state')
        board_utils.drawBoard(b)
        return v_train

    def v_hat(self, b):
        return board_utils.evaluateBoardState(b, self.w, expressivity='compact')
