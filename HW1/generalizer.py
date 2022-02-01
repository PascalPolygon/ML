from board_utils import BoardUtils

board_utils = BoardUtils()


class Generalizer:
    def __init__(self):
        self.w = []
        self.verbose = False

    def LMSWeightUpdate(self, weights, boards, v_trains, lr=0.01):
        error = 0
        for b, v_train in zip(boards, v_trains):
            x1, x2, min_x_to_v, min_o_to_v = board_utils.getStateFeatures(
                b, expressivity='compact')
            xs = [x1, x2, min_x_to_v, min_o_to_v]
            # print(f'Eval weights: {weights}')
            v_hat = board_utils.evaluateBoardState(
                b, weights, expressivity='compact')
            if self.verbose:
                print(f'v_train : {v_train} | v_hat : {v_hat}')
            error += (v_train - v_hat)**2
            # Update weights
            for i in range(len(weights)):
                if i == 0:
                    weights[i] = weights[i] + lr*(v_train - v_hat)*1
                else:
                    # print(xs)
                    weights[i] = weights[i] + lr*(v_train - v_hat)*xs[i-1]

            # print(f'error = {error}')

        return weights, error
