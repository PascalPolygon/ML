from email.policy import default
import os
import inspect
from net import Net
from utils import Utils
import matplotlib.pyplot as plt
import random
import argparse
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

def corrupt_data(inputs, outputs, percent):
    nSamples = len(inputs)
    nCorrupted = math.floor(nSamples*percent)-1
    # utils.log('nCorrupted', nCorrupted)
    alreadyCorrupted = []
    while (len(alreadyCorrupted) < nCorrupted): # Randomly select nCcorrupted samples and corrupt them
        corruptId = random.randint(0, nSamples-1)
        if corruptId in alreadyCorrupted:
            continue

        alreadyCorrupted.append(corruptId)
        options = [[1,0,0],[0,1,0],[0,0,1]]
        options.remove(outputs[corruptId])
        outputs[corruptId] = options[random.randint(0,1)]
    # utils.log('len(alreadyCorrupted)', len(alreadyCorrupted))
    return inputs, outputs

def get_validation(inputs, outputs, percent):
    nSamples = len(inputs)
    utils.log('percent', percent)
    # nValidation = int(nSamples*float(percent))
    nValidation = math.floor(nSamples*float(percent))-1
    utils.log('nValidation', nValidation)
    valInputs = []
    valOutputs = []
    validationIds = []

    while len(validationIds) <= nValidation:
        #Randomly select a row
        valId = random.randint(0, nSamples-1)
        if valId in validationIds:
            continue
        validationIds.append(valId)
        valInputs.append(inputs[valId])
        valOutputs.append(outputs[valId])

    trainInputs = []
    trainOutputs = []
    #Remove validationIds from training data
    for id in range(len(inputs)):
        if id in validationIds:
            #This is a validation id, do not copyt o training inputs
            continue
        #This is a training id
        trainInputs.append(inputs[id])
        trainOutputs.append(outputs[id])
    
    return valInputs, valOutputs, trainInputs, trainOutputs

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_iter", help="max training iterations", default=500)
    parser.add_argument("--lr", help="learning rate", default=0.1)
    parser.add_argument("--hidden_units", help="number of hidden units", default=3)
    parser.add_argument("--validation", help="percentage of data to keep for validation", default=0)
    parser.add_argument("--custom_arch", help="customer hidden layers architecture", default=[3])
    parser.add_argument("--verbose", help="verbose", default=False)
    return parser.parse_args()


if __name__ == '__main__':
    opt = arg_parse() # get hyper-parameters

    if opt.verbose == 'False':
        opt.verbose = False
    elif opt.verbose =='True':
        opt.verbose = True

    # inputs, outputs = get_data(IRIS_TRAIN_FILE)
    # inputs, outputs = corrupt_data(inputs, outputs, 0.2)
    # valInputs, valOutputs, trainInputs, trainOutputs = get_validation(inputs, outputs, opt.validation)

    # utils.log('len(valInputs)', len(valInputs))
    # utils.log('len(trainInputs)', len(trainInputs))
    # utils.log('len(valOutputs)', len(valOutputs))
    # utils.log('len(trainOutputs)', len(trainOutputs))
    # Without a validation set
    noiseLevel = 0
    while (noiseLevel <= 0.2):
        inputs, outputs = get_data(IRIS_TRAIN_FILE)
        inputs, outputs = corrupt_data(inputs, outputs, noiseLevel)
        # trainInputs = inputs
        # trainOutputs = outputs

        # utils.log('trainInputs', trainInputs)
        # utils.log('trainOutputs', trainOutputs)
        valInputs, valOutputs, trainInputs, trainOutputs = get_validation(inputs, outputs, opt.validation)
        # utils.log('len(valInputs)', len(valInputs))
        # utils.log('len(trainInputs)', len(trainInputs))
        # utils.log('len(valOutputs)', len(valOutputs))
        # utils.log('len(trainOutputs)', len(trainOutputs))
        utils.log('Noise Level', noiseLevel)

        n_in = len(trainInputs[0])
        n_out = len(trainOutputs[0])
        net = Net([n_in, int(opt.hidden_units), n_out], lr=float(opt.lr), maxEpoch=int(opt.max_iter), verbose=bool(opt.verbose)) #2 units in input, 3 in hiddel and 1 in output layer
        # utils.log('Training...', None)
        print('Training...')
        net.train(trainInputs, trainOutputs, validationSet=[valInputs, valOutputs], lossThresh=5)
        # net.train(trainInputs, trainOutputs)

        # #calculate accuracy
        acc = calculate_accuracy(trainInputs, trainOutputs)
        utils.log('Train Acc', acc)
        # print('-'*50)
        inputs, outputs = get_data(IRIS_TEST_FILE)
        acc = calculate_accuracy(inputs, outputs)
        utils.log('Test Acc', acc)

        noiseLevel += 0.02
        print('='*50)

# if __name__ == '__main__':
#     opt = arg_parse() # get hyper-parameters
#     inputs, outputs = get_data(IRIS_TRAIN_FILE)
    

#     utils.log('input', inputs)
#     utils.log('output', outputs)

#     n_in = len(inputs[0])
#     n_out = len(outputs[0])

#     net = Net([n_in, int(opt.hidden_units), n_out], lr=float(opt.lr), maxEpoch=int(opt.max_iter), verbose=bool(opt.verbose)) #2 units in input, 3 in hiddel and 1 in output layer
#     net.train(inputs, outputs)

#     plt.plot(net.lossHistory)
#     plt.show()

#     # #calculate accuracy
#     acc = calculate_accuracy(inputs, outputs)
#     utils.log('Train Acc', acc)
#     print('-'*50)
#     inputs, outputs = get_data(IRIS_TEST_FILE)
#     acc = calculate_accuracy(inputs, outputs)
#     utils.log('Test Acc', acc)




