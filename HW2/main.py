import os
from learner import Learner

TENNIS_ATTR_FILE = os.getcwd()+'/tennis-attr.txt'
TENNIS_TRAIN_FILE = os.getcwd()+'/tennis-train.txt'

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
    for i, val in enumerate(tree.values):
        if tree.values[val] is not None:
            valuesList = list(tree.values[val].values.items())
            if valuesList:  # Not a leaf node
                print('|\t' * level + str(tree.attr) + ' = ' + val)
                print_tree(tree.values[val], level+1)
            else:  # This is a leaf node
                print('|\t' * level + str(tree.attr) + ' = ' +
                      val + ' : ' + tree.values[val].attr)


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
    # print("Hello world!")
    testTree = build_tree()
    print_tree(testTree)
    attrs, target = load_attributes(TENNIS_ATTR_FILE)
    learner = Learner(target)
    # attrs, target = load_attributes(IRIS_ATTR_FILE)
    trainingExamples = load_examples(TENNIS_TRAIN_FILE)
    # trainingExamples = load_examples(IRIS_TRAIN_FILE)
    print(f'Target: {target}')
    print(trainingExamples)
    print(learner.build_tree(trainingExamples))
