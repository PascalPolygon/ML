import os
import inspect
from net import Net
from utils import Utils
import matplotlib.pyplot as plt
import math

utils = Utils()

IRIS_TRAIN_FILE = os.getcwd()+'/iris-train.txt'
IRIS_TEST_FILE = os.getcwd()+'/iris-test.txt'

# IDENTITY_TRAIN_FILE = os.getcwd()+'/identity-train.txt'
# IDENTITY_TEST_FILE

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def calculate_accuracy(inputs, targets):
    # predictions = []
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

def process_iris_output(outputs):
    for i in range(len(outputs)):
        if outputs[i] == 'Iris-setosa':
            outputs[i] = [1,0,0]
        elif outputs[i] == 'Iris-versicolor':
            outputs[i] = [0,1,0]
        elif outputs[i] == 'Iris-virginica':
            outputs[i] = [0,0,1]
    return outputs

def get_data(path):
    data = utils.load_examples(path)
    inputs = []
    outputs = []
    # utils.log('data', data)
    for example in data:
        inputs.append(example[:-1])
        outputs.append(example[-1])

    return utils.toFloat(inputs), process_iris_output(outputs)

if __name__ == '__main__':
    inputs, outputs = get_data(IRIS_TRAIN_FILE)
    

    utils.log('input', inputs)
    utils.log('output', outputs)

    n_in = len(inputs[0])
    n_out = len(outputs[0])
    

    # lr  = 0.1
    # me = 150
    net = Net([n_in, 3, n_out], lr=0.1, maxEpoch=1000, verbose=True) #2 units in input, 3 in hiddel and 1 in output layer
    net.train(inputs, outputs)

    plt.plot(net.lossHistory)
    plt.show()

    # #calculate accuracy
    acc = calculate_accuracy(inputs, outputs)
    utils.log('Train Acc', acc)
    print('-'*50)
    inputs, outputs = get_data(IRIS_TEST_FILE)
    acc = calculate_accuracy(inputs, outputs)
    utils.log('Test Acc', acc)

