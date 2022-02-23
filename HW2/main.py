import os
from learner import Learner
from data_utils import DataUtils
from testTennis import TestTennis

TENNIS_ATTR_FILE = os.getcwd()+'/tennis-attr.txt'
TENNIS_TRAIN_FILE = os.getcwd()+'/tennis-train.txt'

# TENNIS_ATTR_FILE = os.getcwd()+'/tennis-attr.txt'
TENNIS_TEST_FILE = os.getcwd()+'/tennis-test.txt'

TENNIS_TRAIN_FILE_PURE = os.getcwd()+'/tennis-train-pure.txt'

IRIS_ATTR_FILE = os.getcwd()+'/iris-attr.txt'
IRIS_TRAIN_FILE = os.getcwd()+'/iris-train.txt'
IRIS_TRAIN_FILE_DEV= os.getcwd()+'/iris-train-dev.txt'



class Node:
    def __init__(self, attr, attrVals):
        self.attr = attr
        self.values = {}
        if attrVals is not None:
            for v in attrVals:
                self.values[v] = None


outlookValues = ["sunny", "overcast", "rain"]
tempValues = ['hot', 'mild', 'cool']
humidityValues = ['high', 'normal']
windValues = ['weak', 'strong']


def build_tree():
    root = Node("Outlook", outlookValues)

    root.values['sunny'] = Node("Temperature", tempValues)
    root.values['sunny'].values['hot'] = Node("Humidity", humidityValues)
    root.values['sunny'].values['hot'].values["high"] = Node(
        "Wind", windValues)
    root.values['sunny'].values['hot'].values["high"].values["strong"] = Node(
        "No", None)
    root.values['sunny'].values['hot'].values["high"].values["weak"] = Node(
        "Yes", None)

    root.values['sunny'].values['cool'] = Node("Wind", windValues)
    root.values['sunny'].values['cool'].values['weak'] = Node("Yes", None)
    root.values['sunny'].values['cool'].values['strong'] = Node("No", None)

    root.values['overcast'] = Node("No", None)
    root.values['rain'] = Node("Yes", None)

    return root

# Pre-order printing

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
    attrs, target = load_attributes(IRIS_ATTR_FILE)

    # trainingExamples = load_examples(TENNIS_TRAIN_FILE)
    # attrs, target = load_attributes(TENNIS_ATTR_FILE)

    learner = Learner(target, verbose=False)
    dataUtils = DataUtils()
    testTennis = TestTennis()
    attrsIndex = {}
    for i, attr in enumerate(attrs):
        attrsIndex[attr] = i
    keyList = list(attrs)

    # print(attrs[keyList[0]][0])
    if attrs[keyList[0]][0] == 'continuous':
        print('Continous data!')
        #Build tree with continous build_tree function
        labels = dataUtils.get_labels(trainingExamples)
        root = learner.build_cont_tree(trainingExamples, target, attrsIndex, attrs)
        print(f'{TAG} Learned tree - ')
        print('-------------------------')
        dataUtils.print_tree(root)
        # print(root)
        print('-------------------------')
        # rules = dataUtils.make_rules(root)
        dataUtils.make_rules('', root)
        # print(dataUtils.globalRules)
        for rule in dataUtils.globalRules:
            print(rule)
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
