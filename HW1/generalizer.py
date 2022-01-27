from board_utils import BoardUtils

board_utils = BoardUtils()


class Generalizer:
    def __init__(self):
        self.w = []

    def LMSWeightUpdate(self, weights, boards, v_trains, lr=0.01):
        for b, v_train in zip(boards, v_trains):
            x1, x2, min_x_to_v, min_o_to_v = board_utils.getStateFeatures(
                b, expressivity='compact')
            xs = [x1, x2, min_x_to_v, min_o_to_v]
            v_hat = board_utils.evaluateBoardState(
                b, weights, expressivity='compact')
            for i in range(len(weights)):
                if i == 0:
                    weights[i] = weights[i] + lr*(v_train - v_hat)*1
                else:
                    # print(xs)
                    weights[i] = weights[i] + lr*(v_train - v_hat)*xs[i-1]
        return weights
