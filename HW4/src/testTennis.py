import os
from utils import Utils
from gabil import Gabil

TENNIS_TRAIN_FILE = os.getcwd()+'/../data/tennis-train.txt'
TENNIS_TEST_FILE = os.getcwd()+'/../data/tennis-test.txt'

utils = Utils()

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
            # inputs[i][2] = [0,1]
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

def evaluate(P, inputs, targets):
    nCorrects = 0
    for h in P:
        nCorrects += gabil.correct_tennis(h, inputs, targets)
    acc = nCorrects/len(inputs)
    if acc > 1.0:
        return 1.0
    else :
        return acc
if __name__ == "__main__":
    opt = utils.arg_parse() # get hyper-parameters
    utils.log('opt', opt)
    # hidden_arch = utils.get_hidden_arch(opt.hidden_arch) #forma user-defined hidden architecture
    
    inputs, outputs = get_data(TENNIS_TRAIN_FILE)
    testInputs, testOutputs = get_data(TENNIS_TEST_FILE)

    gabil = Gabil(inputs, outputs, verbose=opt.verbose)
    # q = int(len(inputs)/2) #Max num of hypothesis
    q = 8 # n individual rules
    utils.log('max_hypothesis', q)
    # p = 2 # 2 rules in first hypothesis, 3 is second
    # p = 5 #nHypothesese
    p = None

    P = -1
    while P == -1:
        P = gabil.tennis(float(opt.fitness_thresh), q, p, float(opt.r), float(opt.m), int(opt.max_gen))
    # utils.log(f'Learned hypotheses {len(P)}')
    # totalLen = 0
    # for i, h in enumerate(P):
    #     utils.log(f'h{i}', h)
    #     totalLen += len(h)
    # utils.log('n_rules', totalLen/11)
    readable_rules = utils.display_tennis_rules(P)
    for i, hypo_rule in enumerate(readable_rules):
        print(f'h{i}')
        for j, rule in enumerate(hypo_rule):
            if j == 0:
                print(rule)
            else:
                print(' V ' + rule)
        print('-'*100)

    #Print acc
    acc = evaluate(P, inputs, outputs)
    utils.log('train acc', acc)
    acc = evaluate(P, testInputs, testOutputs)
    utils.log('test acc', acc)
    # print(inputs)
    # print(outputs)
    # n_in = len(inputs[0])
    # n_out = len(outputs[0])