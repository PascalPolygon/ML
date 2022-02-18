from node import Node
from data_utils import DataUtils
# data_utils = DataUtils()

dataUtils = DataUtils(verbose=True)


class Learner():

    def __init__(self, target, verbose=False):
        self.target = target
        self.verbose = verbose

    def build_tree(self, trainingExamples, targetAttribute, attributes, attrsIndex):
        # Create a root node
        root = Node(None, None)
        labels = dataUtils.get_labels(trainingExamples)

        # if self.verbose:
        #     print(labels)
        #     print(f'Target attr: {targetAttribute}')
        #     print(f'Attributes: {attributes}')
        # print(f'Target attribute: {list(attributes)[-1]}')

        isPure, targetLabel = self.check_purity(labels)

        if self.verbose:
            print(f'Labels purity: {isPure},\ntargetLabel: {targetLabel}')

        if isPure:
            print(f'Is pure! returning')
            print(labels)
            return Node(targetLabel, None)

        if not attributes:
            # Return single-node tree root, with label = most common value of Target-attribute
            mCommonLabel = dataUtils.get_mcommon_label(labels)
            return Node(mCommonLabel, None)

        # Begin main algorithm
        # Find attribute with highest info gain
        print(f'BUILD-TREE - find best attr: {attributes}')
        bestAttr = dataUtils.find_best_attr(
            trainingExamples, attributes, labels, attrsIndex)
        print(f'BUILD-TREE - new best attr: {bestAttr}')

        root = Node(bestAttr, attributes[bestAttr])
        # print(trainingExamples)

        for val in attributes[bestAttr]:
            # Get example subsets that have value = val
            examplesVal = dataUtils.get_val_examplesubsset(
                val, trainingExamples)
            if not examplesVal:
                # print(f'BUILD-TREE - most common label: {mCommonLabel}')
                mCommonLabel = dataUtils.get_mcommon_label(labels)
                print(f'BUILD-TREE - most common label: {mCommonLabel}')
                # Node(mCommonLabel, None)
                root.values[val] = Node(mCommonLabel, None)
            else:
                # Remove the current best attribute because we already used it
                print(f'BUILD-TREE - attributes: {attributes}')
                print(f'BUILD-TREE - bestAttr {bestAttr}')
                print(f'BUILD-TREE - ***branch***: {val}')
                # del attributes[bestAttr]
                newAttributes = attributes.copy()
                del newAttributes[bestAttr]
                root.values[val] = self.build_tree(
                    examplesVal, targetAttribute, newAttributes, attrsIndex)
        return root
        #tree = self.id3(traning_examples)
        # return tree
    # def isPure(self, data):

    def check_purity(self, labels):
        length = len(labels)
        targetLabel = labels[0]
        labelLen = 0
        for labl in labels:
            if labl == targetLabel:
                # print(f'{labl} == {targetLabel}')
                labelLen += 1
        return (labelLen == length), targetLabel
