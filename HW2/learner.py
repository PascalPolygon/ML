from node import Node
from data_utils import DataUtils
# data_utils = DataUtils()

dataUtils = DataUtils(verbose=True)


class Learner():

    def __init__(self, target, verbose=False):
        self.target = target
        self.verbose = verbose

    def build_tree(self, trainingExamples, targetAttribute, attributes):
        # Create a root node
        root = Node(None, None)
        # Check if all examles are of the same label, retrun the label if that's the case
        # print(trainingExamples)
        # adataUtils.split_data(trainingExamples)
        labels = dataUtils.get_labels(trainingExamples)

        if self.verbose:
            print(labels)
            print(f'Target attr: {targetAttribute}')
            print(f'Attributes: {attributes}')

        isPure, targetLabel = self.check_purity(labels)

        if self.verbose:
            print(f'Labels purity: {isPure},\ntargetLabel: {targetLabel}')

        if isPure:
            return Node(targetLabel, None)

        if not attributes:
            # Return single-node tree root, with label = most common value of Target-attribute
            mCommonLabel = dataUtils.get_mcommon_label(labels)
            return Node(mCommonLabel, None)

        # Begin main algorithm
        # Find attribute with highest info gain
        dataUtils.find_best_attr(trainingExamples, attributes)

        # self.isPure(labels)
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
