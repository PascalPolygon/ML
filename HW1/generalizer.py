class Generalizer:
    def __init__(self):
        self.w = []

    def LMSWeightUpdate(self, weights, boards, v_trains, eta=0.01):
        for b, v_train in zip(boards, v_trains):
            xs = board_utils.getStateFeatures(b)
            v_hat = board_utils.evaluateBoardState(
                b, weights, expressivity='compact')
            for i, w in enumerate(weights):
                w = w + eta(v_train - v_hat)*xs[i]
        return w
