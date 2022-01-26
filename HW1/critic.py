class Critic:
    def __init__(self):
        self.data = []

    def getTrainingExamples(self, gameHistory, w):
        size = len(gameHistory)
        for i in range(size):
            b = gameHistory[size-1]  # Final board state
            v_train = self.getScore(b)
