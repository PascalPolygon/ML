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

    def LMSWeightUpdateFull(self, weights, boards, v_trains, lr=0.01):
        error = 0
        for b, v_train in zip(boards, v_trains):
            x1, x2, min_x_to_v, min_o_to_v = board_utils.getStateFeatures(
                b, expressivity='full')

            # rows
            x3 = min_x_to_v[0]
            x4 = min_x_to_v[1]
            x5 = min_x_to_v[2]

            # cols
            x6 = min_x_to_v[3]
            x7 = min_x_to_v[4]
            x8 = min_x_to_v[5]

            # diags
            x9 = min_x_to_v[6]
            x10 = min_x_to_v[7]

            # opponent
            # rows
            x11 = min_o_to_v[0]
            x12 = min_o_to_v[1]
            x13 = min_o_to_v[2]

            # cols
            x14 = min_o_to_v[3]
            x15 = min_o_to_v[4]
            x16 = min_o_to_v[5]

            # diags
            x17 = min_o_to_v[6]
            x18 = min_o_to_v[7]

            # xs = [x1, x2, min_x_to_v, min_o_to_v]
            xs = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10,
                  x11, x12, x13, x14, x15, x16, x17, x18]
            # print(f'Eval weights: {weights}')
            v_hat = board_utils.evaluateBoardState(
                b, weights, expressivity='full')
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
