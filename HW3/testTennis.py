import os
import inspect
from net import Net
from utils import Utils
import matplotlib.pyplot as plt
import math

utils = Utils()

TENNIS_TRAIN_FILE = os.getcwd()+'/tennis-train.txt'
TENNIS_TEST_FILE = os.getcwd()+'/tennis-test.txt'

# IDENTITY_TRAIN_FILE = os.getcwd()+'/identity-train.txt'
# IDENTITY_TEST_FILE

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def calculate_accuracy(inputs, outputs):
    n_correct = 0
    n_samples = len(inputs)
    for inp, target in zip(inputs, outputs):
        pred = net.feedForward(inp)
        pred[0] = round(pred[0])
        if target[0] == pred[0]:
            n_correct += 1
    return n_correct/n_samples

# def disp_net_representation(inputs):
#     print('              Input                      Hidden Values                        Output')
#     for input in inputs:
#         pred = net.feedForward(input)
#         hiddenValues = net.a[-2][:-1] #Second to last of activations are hidden activations, exclude the very last one because it's the bias
#         for i in range(len(pred)):
#             pred[i] = float("{:.1f}".format(pred[i]))
#         thresholded = []
#         for i in range(len(hiddenValues)):
#             hiddenValues[i] = float("{:.2f}".format(hiddenValues[i]))
#             thresholded.append(1 if hiddenValues[i]  >= 0.5 else 0)
#         # print(f'{*input} -> {hiddenValues} ({thresholded}) -> {pred}', sep=" ")
#         print(*input, sep=" ", end=" ")
#         print(' -> ',end=" ")
#         print(*hiddenValues, sep=" ", end=" ")
#         print('(', end="")
#         print(*thresholded, sep=" ", end="")
#         print(')', end=" ")
#         print(' -> ',end=" ")
#         print(*pred, sep=" ")

def process_tennis_data(inputs, outputs):
    for i, input in enumerate(inputs):
        new_input = []
        #Outlook
        if input[0] == 'Sunny':
            # inputs[i][0] = [1,0,0]
            new_input.append(1)
            new_input.append(0)
            new_input.append(0)
        elif input[0] == 'Overcast':
            # inputs[i][0] = [0,1,0]
            new_input.append(0)
            new_input.append(1)
            new_input.append(0)
        elif input[0] == 'Rain':
            # inputs[i][0] = [0,0,1]
            new_input.append(0)
            new_input.append(0)
            new_input.append(1)

        #Temperature
        if input[1] == 'Hot':
            # inputs[i][1] = [1,0,0]
            new_input.append(1)
            new_input.append(0)
            new_input.append(0)
        elif input[1] == 'Mild':
            # inputs[i][1] = [0,1,0]
            new_input.append(0)
            new_input.append(1)
            new_input.append(0)
        elif input[1] == 'Cool':
            # inputs[i][1] = [0,0,1]
            new_input.append(0)
            new_input.append(0)
            new_input.append(1)
        
        #Humidity
        if input[2] == 'High':
            # inputs[i][2] = [1,0]
            new_input.append(1)
            new_input.append(0)
        elif input[2] == 'Normal':
            inputs[i][2] = [0,1]
            new_input.append(0)
            new_input.append(1)
        
        #Wind
        if input[3] == 'Weak':
            # inputs[i][3] = [1,0]
            new_input.append(1)
            new_input.append(0)
        elif input[3] == 'Strong':
            # inputs[i][3] = [0,1]
            new_input.append(0)
            new_input.append(1)

        inputs[i] = new_input
        
    for i in range(len(outputs)):
        outputs[i] = [0] if outputs[i] == 'No' else [1]
    
    return inputs, outputs

def get_data(path):
    data = utils.load_examples(path)
    inputs = []
    outputs = []
    # utils.log('data', data)
    for example in data:
        inputs.append(example[:-1])
        outputs.append(example[-1])

    return process_tennis_data(inputs, outputs)

if __name__ == '__main__':
    inputs, outputs = get_data(TENNIS_TRAIN_FILE)

    utils.log('input', inputs)
    utils.log('output', outputs)

    n_in = len(inputs[0])
    n_out = len(outputs[0])

    # lr  = 0.1
    # me = 150
    net = Net([n_in, 3, n_out], lr=0.1, maxEpoch=50, verbose=True) #2 units in input, 3 in hiddel and 1 in output layer
    # net = Net([n_in, 3, n_out], lr=0.01, maxEpoch=1000, verbose=True) 
    net.train(inputs, outputs)

    plt.plot(net.lossHistory)
    plt.show()

    #calculate accuracy
    acc = calculate_accuracy(inputs, outputs)
    utils.log('Train Acc', acc)
    print('-'*50)
    inputs, outputs = get_data(TENNIS_TEST_FILE)
    acc = calculate_accuracy(inputs, outputs)
    utils.log('Test Acc', acc)
