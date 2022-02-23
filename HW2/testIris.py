import os
from learner import Learner
from data_utils import DataUtils
from testDiscrete import TestTennis
from testContinous import TestIris
from rules_utils import RulesUtils

TENNIS_ATTR_FILE = os.getcwd()+'/tennis-attr.txt'
TENNIS_TRAIN_FILE = os.getcwd()+'/tennis-train.txt'
TENNIS_TEST_FILE = os.getcwd()+'/tennis-test.txt'
# TENNIS_ATTR_FILE = os.getcwd()+'/tennis-attr.txt'


# TENNIS_TRAIN_FILE_PURE = os.getcwd()+'/tennis-train-pure.txt'

IRIS_ATTR_FILE = os.getcwd()+'/iris-attr.txt'
IRIS_TRAIN_FILE = os.getcwd()+'/iris-train.txt'
IRIS_TEST_FILE = os.getcwd()+'/iris-test.txt'
# IRIS_TRAIN_FILE_DEV= os.getcwd()+'/iris-train-dev.txt'



class Node:
    def __init__(self, attr, attrVals):
        self.attr = attr
        self.values = {}
        if attrVals is not None:
            for v in attrVals:
                self.values[v] = None

def load_attributes(file):
    attributes = {}
    targetAttr = ''
    setTarget = False

    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if (line):
                # print(f'AttrElems : {attrElems}')
                attrElems = line.split(' ')
                attributes[attrElems[0]] = attrElems[1:]
                if setTarget:
                    targetAttr = attrElems[0]
                    setTarget = False
            else:
                # Next line is the target attribute
                setTarget = True
    return attributes, targetAttr


def load_examples(file):
    trainingExamples = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            example = line.split(' ')
            trainingExamples.append(example)
    return trainingExamples


if __name__ == '__main__':
    TAG = '__main__'
    dataUtils = DataUtils()
    # root = build_tree()

    # dataUtils.print_tree(root)
    # rules = dataUtils.print_rules('', root)
    trainingExamples = load_examples(IRIS_TRAIN_FILE)
    testExamples = load_examples(IRIS_TEST_FILE)
    attrs, target = load_attributes(IRIS_ATTR_FILE)

    # trainingExamples = load_examples(TENNIS_TRAIN_FILE)
    # attrs, target = load_attributes(TENNIS_ATTR_FILE)
    # testExamples = load_examples(TENNIS_TEST_FILE)

    learner = Learner(target, verbose=False)
    dataUtils = DataUtils()
    testTennis = TestTennis()
    ruleUtils = RulesUtils()
    testIris = TestIris()

    attrsIndex = {}
    for i, attr in enumerate(attrs):
        attrsIndex[attr] = i
    keyList = list(attrs)

    # print(attrs[keyList[0]][0])
    if attrs[keyList[0]][0] == 'continuous':
        # print('Continous data!')
        trainingExamples, validationExamples = dataUtils.split_data(trainingExamples, 0.6666) #keeep ~2/3 of data for training remaining for validation
        # Build tree with continous build_tree function
        labels = dataUtils.get_labels(trainingExamples)
        root = learner.build_cont_tree(trainingExamples, target, attrsIndex, attrs)
        uTargets = attrs[target]
        print(f'{TAG} Learned tree - ')
        print('-------------------------')
        dataUtils.print_tree(root)
        # print(root)
        print('-------------------------')
        # rules = dataUtils.make_rules(root)
        dataUtils.make_rules('', root)
        # print(dataUtils.globalRules)
        # for rule in dataUtils.globalRules:
        #     print(rule)
        trainRuleAccs = []
        testRuleAccs = []

        for rule in dataUtils.globalRules:
            # print(f'{TAG} rule - {rule}')
            trainRuleAccs.append(ruleUtils.test_rule_acc(trainingExamples, rule, attrsIndex))
            testAcc = ruleUtils.test_rule_acc(testExamples, rule, attrsIndex)
            if testAcc is None:
                #This rule is useless for the tests set: (don't use it)
                continue
            else:
                testRuleAccs.append(testAcc)
            # print(f'{TAG} ruleAcc on train - {trainRuleAcc}')
            # print(f'{TAG} ruleAcc on test - {testRuleAcc}')
        print(f'{TAG} Avg rule acc on train - {sum(trainRuleAccs)/len(trainRuleAccs)}')
        print(f'{TAG} Avg rule acc on test - {sum(testRuleAccs)/len(testRuleAccs)}')

        trainAcc = testIris.test(trainingExamples, dataUtils.globalRules, attrsIndex)
        testAcc = testIris.test(testExamples, dataUtils.globalRules, attrsIndex)
        print(f'{TAG} Accuracy on train - {trainAcc}')
        print(f'{TAG} Accuracy on test - {testAcc}')

        pruningExamples = validationExamples
        # pruningExamples = testExamples
        for ruleIdx in range(len(dataUtils.globalRules)):
            acc = ruleUtils.test_rule_acc(pruningExamples, dataUtils.globalRules[ruleIdx], attrsIndex)
            newAcc = 1
            i = 0
            if acc is not None:
                while newAcc > acc:
                    # print(f'ITER :{i}')
                    acc = ruleUtils.test_rule_acc(pruningExamples, dataUtils.globalRules[ruleIdx], attrsIndex)
                    tempRule = ruleUtils.prune_rule(dataUtils.globalRules[ruleIdx], pruningExamples, acc, attrsIndex)
                    newAcc = ruleUtils.test_rule_acc(pruningExamples, tempRule, attrsIndex)
                    if newAcc > acc:
                        dataUtils.globalRules[ruleIdx] = tempRule
                    i += 1
        
        testRuleAccs = []
        for rule in dataUtils.globalRules:
            # print(f'{TAG} rule - {rule}')
            testAcc = ruleUtils.test_rule_acc(testExamples, rule, attrsIndex)
            if testAcc is None:
                #This rule is useless for the tests set: (don't use it)
                continue
            else:
                testRuleAccs.append(testAcc)
        print(f'{TAG} Avg rule acc on test (pruned) - {sum(testRuleAccs)/len(testRuleAccs)}')

        trainAcc = testIris.test(trainingExamples, dataUtils.globalRules, attrsIndex)
        testAcc = testIris.test(testExamples, dataUtils.globalRules, attrsIndex)
        print(f'{TAG} Accuracy on train (pruned) - {trainAcc}')
        print(f'{TAG} Accuracy on test (pruned) - {testAcc}')

    else:
        root = learner.build_tree(trainingExamples, target, attrs, attrsIndex)
        #Load test data
        print(f'{TAG} Learned tree - ')
        print('-------------------------')
        dataUtils.print_tree(root)
        print('-------------------------')

        # rules = dataUtils.make_rules(root)
        dataUtils.make_rules('', root)
        # print(dataUtils.globalRules)
        for rule in dataUtils.globalRules:
            print(rule)

        testExamples = load_examples(TENNIS_TEST_FILE)
        trainAcc = testTennis.test(root, trainingExamples, attrsIndex)
        testAcc = testTennis.test(root, testExamples, attrsIndex)
        print(f'{TAG} Accuracy on train - {trainAcc}')
        print(f'{TAG} Accuracy on test - {testAcc}')
