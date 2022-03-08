import os
import inspect
from net import Net
from utils import Utils
import matplotlib.pyplot as plt

utils = Utils()

TENNIS_TRAIN_FILE = os.getcwd()+'/tennis-train.txt'
TENNIS_TEST_FILE = os.getcwd()+'/tennis-test.txt'

IDENTITY_TRAIN_FILE = os.getcwd()+'/identity-train.txt'
# IDENTITY_TEST_FILE

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def calculate_accuracy(inputs, targets):
    predictions = []
    n_correct = 0
    n_samples = 0
    for inp, target in zip(inputs, targets):
        n_samples += 1
        pred = (net.feedForward(inp))
        
        for i in range(len(pred)):
            pred[i] = float("{:.1f}".format(pred[i]))

        true_max = target.index(max(target))
        pred_max = pred.index(max(pred))

        if true_max == pred_max:
            n_correct += 1
        # print('------------------')
    return n_correct/n_samples


if __name__ == '__main__':
    data = utils.load_examples(IDENTITY_TRAIN_FILE)
    inputs = []
    outputs = []
    for example in data:
        inputs.append(example[:8])
        outputs.append(example[9:])
    #Convert to float
    inputs = utils.toFloat(inputs)
    outputs = utils.toFloat(outputs)

    # utils.log('intput', inputs)
    # utils.log('output', outputs)

    n_in = len(inputs[0])
    n_out = len(outputs[0])

    net = Net([n_in, 3, n_out], lr=5, maxEpoch=200) #2 units in input, 3 in hiddel and 1 in output layer

    net.train(inputs, outputs)

    plt.plot(net.lossHistory)
    plt.show()

    acc = calculate_accuracy(inputs, outputs)
    utils.log('Train Acc', acc)
    utils.log('Hidden Values', net.a)

