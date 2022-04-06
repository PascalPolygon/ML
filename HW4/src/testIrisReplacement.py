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
    opt = utils.arg_parse() # get hyper-parameters
    inputs, targets = get_data(IRIS_TRAIN_FILE)
    testInputs, testTargets = get_data(IRIS_TEST_FILE)
    # print(testInputs)
    gabil = Gabil(inputs, targets, verbose=opt.verbose)

    allResults = []
    rs = []
    r = 0
    while r <= 0.85:
        r += 0.1
        rs.append(r)
        p = None

        results = []
        print('='*50)
        P = -1
        utils.log('USING FITNESS_PROPORTIONAL')
        while P == -1:
            if opt.fitness_thresh is not None:
                P = gabil.irisSelection(float(opt.fitness_thresh), int(opt.q), p, r, float(opt.m), int(opt.max_gen), 'fitness_proportional')
            else:
                P = gabil.irisSelection(None, int(opt.q), p, r, float(opt.m), int(opt.max_gen), 'fitness_proportional')
        acc = evaluate(P, inputs, targets)
        results.append(acc)
        utils.log('r', r)
        utils.log('train acc', acc)
        acc = evaluate(P, testInputs, testTargets)
        results.append(acc)
        utils.log('test acc', acc)
        
        print('='*50)
        P = -1
        utils.log('USING TOURNAMENT_SELECTION')
        while P == -1:
            if opt.fitness_thresh is not None:
                P = gabil.irisSelection(float(opt.fitness_thresh), int(opt.q), p, r, float(opt.m), int(opt.max_gen), 'tournament')
            else:
                P = gabil.irisSelection(None, int(opt.q), p, r, float(opt.m), int(opt.max_gen), 'tournament')
        acc = evaluate(P, inputs, targets)
        results.append(acc)
        utils.log('r', r)
        utils.log('train acc', acc)
        acc = evaluate(P, testInputs, testTargets)
        results.append(acc)
        utils.log('test acc', acc)


        print('='*50)
        P = -1
        utils.log('USING RANK_SELECTION')
        while P == -1:
            if opt.fitness_thresh is not None:
                P = gabil.irisSelection(float(opt.fitness_thresh), int(opt.q), p, r, float(opt.m), int(opt.max_gen), 'rank')
            else:
                P = gabil.irisSelection(None, int(opt.q), p, r, float(opt.m), int(opt.max_gen), 'rank')
        acc = evaluate(P, inputs, targets)
        results.append(acc)
        utils.log('r', r)
        utils.log('train acc', acc)
        acc = evaluate(P, testInputs, testTargets)
        results.append(acc)
        utils.log('test acc', acc)

        allResults.append(results)

    # print('='*54)
    # print('='*50)
    # print('                           train acc       |      test acc')
    # print(f'FITNESS_PROPORTIONAL | {results[0]*100} % | {results[1]*100} %')
    # print(f'TOURNAMENT_SELECTION | {results[2]*100} % | {results[3]*100} %')
    # print(f'FITNESS_PROPORTIONAL | {results[4]*100} % | {results[5]*100} %')

    # results = [0.9,0.5,0.3,0.2,0.4,0.4]
    for results, r in zip(allResults, rs):
        print('-'*54)
        print(f'REPLACEMENT RATE = {r}')
        print('                           | train acc      | test acc')
        print('-'*54)
        print(f'FITNESS_PROPORTIONAL       | {results[0]*100} %          | {results[1]*100} %')
        print(f'TOURNAMENT_SELECTION       | {results[2]*100} %          | {results[3]*100} %')
        print(f'FITNESS_PROPORTIONAL       | {results[4]*100} %          | {results[5]*100} %')