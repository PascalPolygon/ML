from node import Node
from data_utils import DataUtils
# data_utils = DataUtils()

dataUtils = DataUtils(verbose=False)


class Learner():

    def __init__(self, target, verbose=False):
        self.target = target
        self.verbose = verbose

    def build_tree(self, trainingExamples, targetAttribute, attributes, attrsIndex):
        # # Create a root node
        # root = Node(None, None)
        TAG = 'BUILD-TREE'
        labels = dataUtils.get_labels(trainingExamples)
        # Check if attributes are continous. If they are: Do proper splitting and copy over all the other attrvalues. This is because continuous attributes must compete with all other attribtues
        attributes = dataUtils.get_cont_attrVals(attributes, trainingExamples, labels, targetAttribute)
        print(f'{TAG} attributes - {attributes}')

        # isPure, targetLabel = self.check_purity(labels)

        # if self.verbose:
        #     print(f'Labels purity: {isPure},\ntargetLabel: {targetLabel}')

        # if isPure:
        #     return Node(targetLabel, None)
        # print(f'BUILD-TREE: {attributes}')
        # if not attributes:
        #     # Return single-node tree root, with label = most common value of Target-attribute
        #     mCommonLabel = dataUtils.get_mcommon_label(labels)
        #     return Node(mCommonLabel, None)

        # # Begin main algorithm
        # # Find attribute with highest info gain
        # bestAttr = dataUtils.find_best_attr(
        #     trainingExamples, attributes, labels, attrsIndex)

        # root = Node(bestAttr, attributes[bestAttr])
        # #TODO: For a continous attribute, you would would all the attribute values from all the current attributes as branchces
        # # print(trainingExamples)

        # for val in attributes[bestAttr]:
        #     # Get example subsets that have value = val
        #     examplesVal = dataUtils.get_val_examplesubsset(
        #         val, trainingExamples)
        #     # TODO: Make sure this works for continous values
        #     if not examplesVal:
        #         mCommonLabel = dataUtils.get_mcommon_label(labels)
        #         root.values[val] = Node(mCommonLabel, None)
        #     else:
        #         # Remove the current best attribute because we already used it
        #         if self.verbose:
        #             print(f'BUILD-TREE - attributes: {attributes}')
        #             print(f'BUILD-TREE - bestAttr {bestAttr}')
        #             print(f'BUILD-TREE - ***branch***: {val}')
        #         newAttributes = attributes.copy()
        #         del newAttributes[bestAttr]
        #         root.values[val] = self.build_tree(
        #             examplesVal, targetAttribute, newAttributes, attrsIndex)
        # return root

    def check_purity(self, labels):
        length = len(labels)
        targetLabel = labels[0]
        labelLen = 0
        for labl in labels:
            if labl == targetLabel:
                # print(f'{labl} == {targetLabel}')
                labelLen += 1
        return (labelLen == length), targetLabel
