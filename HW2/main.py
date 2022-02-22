import os
from learner import Learner
from data_utils import DataUtils

TENNIS_ATTR_FILE = os.getcwd()+'/tennis-attr.txt'
TENNIS_TRAIN_FILE = os.getcwd()+'/tennis-train.txt'
TENNIS_TRAIN_FILE_PURE = os.getcwd()+'/tennis-train-pure.txt'

IRIS_ATTR_FILE = os.getcwd()+'/iris-attr.txt'
IRIS_TRAIN_FILE = os.getcwd()+'/iris-train.txt'


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
        "n", None)
    root.values['sunny'].values['hot'].values["high"].values["weak"] = Node(
        "y", None)

    root.values['sunny'].values['cool'] = Node("Wind", windValues)
    root.values['sunny'].values['cool'].values['weak'] = Node("y", None)
    root.values['sunny'].values['cool'].values['strong'] = Node("n", None)

    root.values['overcast'] = Node("n", None)
    root.values['rain'] = Node("y", None)

    return root

# Pre-order printing


def print_tree(tree, level=0):
    if tree == None:
        return
    if tree.values:
        for i, val in enumerate(tree.values):
            if tree.values[val] is not None:
                valuesList = list(tree.values[val].values.items())
                if valuesList:  # Not a leaf node
                    print('|\t' * level + str(tree.attr) + ' = ' + val)
                    print_tree(tree.values[val], level+1)
                else:  # This is a leaf node
                    print('|\t' * level + str(tree.attr) + ' = ' +
                          val + ' : ' + tree.values[val].attr)
    else:
        print('|\t' * level + str(tree.attr))


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

    # trainingExamples = load_examples(TENNIS_TRAIN_FILE)
    # attrs, target = load_attributes(TENNIS_ATTR_FILE)

    trainingExamples = load_examples(IRIS_TRAIN_FILE)
    attrs, target = load_attributes(IRIS_ATTR_FILE)

    print(f'Target: {target}')
    learner = Learner(target, verbose=False)
    dataUtils = DataUtils()
    # print(f'Target: {target}')
    # print(trainingExamples)
    # c = list(attrs).index(attr)
    # Make dictionaly of attributes and their index
    attrsIndex = {}
    for i, attr in enumerate(attrs):
        attrsIndex[attr] = i
    print(f'__MAIN__ - attrIndex: {attrsIndex}')
    print(f'__MAIN__ - attrs: {attrs}')
    # Check if attributes are continuous
    keyList = list(attrs)

    # print(attrs[keyList[0]][0])
    if attrs[keyList[0]][0] == 'continuous':
        print('Continous data!')
        #Build tree with continous build_tree function
        labels = dataUtils.get_labels(trainingExamples)
        attrs = dataUtils.get_cont_attrVals(attrs, trainingExamples, labels, target, attrsIndex)
        print(f'__MAIN__ - contAttrs: {attrs}')
        root = learner.build_cont_tree(trainingExamples, target, attrs, attrsIndex)
    else:
        root = learner.build_tree(trainingExamples, target, attrs, attrsIndex)
    # print(root.attr)
    # print(root.values)
    print_tree(root)
