from utils import Utils
import os
import copy
from gabil import Gabil
from concurrent.futures import ThreadPoolExecutor

utils = Utils()

IRIS_TRAIN_FILE = os.getcwd()+'/../data/iris-train.txt'
IRIS_TEST_FILE = os.getcwd()+'/../data/iris-test.txt'


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
    lilahFactor = 10
    return utils.toBin(inputs, lilahFactor), process_iris_output(outputs)

def evaluate(P, inputs, targets):
    nCorrects = 0
    for h in P:
        nCorrects += gabil.correct_iris(h, inputs, targets)
    acc = nCorrects/len(inputs)
    if acc > 1.0:
        return 1.0
    else :
        return acc

if __name__ == '__main__':
    #Good res with:
    # C:/Python/python.exe c:/ML/HW4/src/testIris.py --fitness_thresh 500
    opt = utils.arg_parse() # get hyper-parameters
    inputs, targets = get_data(IRIS_TRAIN_FILE)
    testInputs, testTargets = get_data(IRIS_TEST_FILE)
    # print(testInputs)
    gabil = Gabil(inputs, targets, verbose=opt.verbose)

    p = None

    P = -1
    while P == -1:
        executor = ThreadPoolExecutor(max_workers=50)
        future = executor.submit(gabil.irisSelection, float(opt.fitness_thresh), int(opt.q), p, float(opt.r), float(opt.m), int(opt.max_gen), opt.sel_strategy)
        #  P = gabil.irisSelection(None, int(opt.q), p, float(opt.r), float(opt.m), int(opt.max_gen), 'rank')
        P = future.result()
        # print(P)
        # P = gabil.iris(float(opt.fitness_thresh), q, p, float(opt.r), float(opt.m), int(opt.max_gen))

    readable_rules = utils.display_iris_rule(P)
    for i, hypo_rule in enumerate(readable_rules):
        print(f'h{i}')
        for j, rule in enumerate(hypo_rule):
            if j == 0:
                print(rule)
            else:
                print(' V ' + rule)
        print('-'*100)

    acc = evaluate(P, inputs, targets)
    utils.log('train acc', acc)
    acc = evaluate(P, testInputs, testTargets)
    utils.log('test acc', acc)