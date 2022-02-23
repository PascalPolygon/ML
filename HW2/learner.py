from node import Node
from data_utils import DataUtils
# data_utils = DataUtils()

dataUtils = DataUtils(verbose=False)


class Learner():

    def __init__(self, target, verbose=False):
        self.target = target
        self.verbose = verbose

    # def build_cont_tree(self, trainingExamples, targetAttribute, attributes, attrsIndex):
    #     TAG = 'BUILD-CONT-TREE'
    #     print('---------------------------------------')
    #     print('---------------------------------------')
    #     labels = dataUtils.get_labels(trainingExamples)
    #     print(f'{TAG} trainingExamples len - {len(trainingExamples)}')
    #     print(f'{TAG} labels len - {len(labels)}')
    #     # Check if attributes are continous. If they are: Do proper splitting and copy over all the other attrvalues. This is because continuous attributes must compete with all other attribtues
    #     # print(f'{TAG} attributes - {attributes}')
    #     keyList = list(attributes)
    #     anyContAttr = keyList[0]
    #     inputAttrs = attributes[anyContAttr]
    #     # inputAttributes = dataUtils.get_cont_input_attrs(attributes, targetAttribute)
    #     # print(f'{TAG} inputAttributes - {inputAttrs}')
    #     isPure, targetLabel = self.check_purity(labels)

    #     if self.verbose:
    #         print(f'Labels purity: {isPure},\ntargetLabel: {targetLabel}')

    #     if isPure:
    #         return Node(targetLabel, None)
    #     # print(f'BUILD-TREE: {attributes}')
    #     if not attributes[anyContAttr]:
    #         # Return single-node tree root, with label = most common value of Target-attribute
    #         uTargets = attributes[targetAttribute]
    #         mCommonLabel = dataUtils.get_mcommon_label(labels, uTargets)
    #         return Node(mCommonLabel, None)
    #     # attributes = dataUtils.get_cont_attrVals(attributes, trainingExamples, labels, targetAttribute, attrsIndex)
    #     # print(f'{TAG} attributes (after get_cont_attrVals) - {attributes}')
      
    #     # TODO: Edit to accomodate thresholds
    #     bestAttr = dataUtils.find_best_attr(
    #         trainingExamples, attributes, labels, attrsIndex)
    #     # print(f'{TAG} (before) inputAttrs - {inputAttrs}')
    #     inputAttrs.remove(bestAttr) #Remove bestAttr from inputAttrs
        
    #     print(f'{TAG} bestAttr - {bestAttr}')
    #     # print(f'{TAG} inputAttrs - {inputAttrs}')
    #     root = Node(bestAttr, inputAttrs)
    #     # print(f'{TAG} node attribute - {root.attr}')
    #     # print(f'{TAG} node values - {root.values}')
    #     # #TODO: For a continous attribute, you would would all the attribute values from all the current attributes as branchces
    #     # # print(trainingExamples)
    #     print(f'{TAG} inputAttributes - {inputAttrs}')
    #     for attrVal in inputAttrs:
    #         print(f'{TAG} attrVal - {attrVal}')
    #         # examplesVal, _ = dataUtils.get_passing_cont_values(attrVal, trainingExamples, attrsIndex)
    #         examplesVal = dataUtils.get_passing_training_examples(attrVal, trainingExamples, attrsIndex)
    #         print(f'{TAG} passing examples - {len(examplesVal)}')
    #         if not examplesVal:
    #             uTargets = attributes[targetAttribute]
    #             mCommonLabel = dataUtils.get_mcommon_label(labels, uTargets)
    #             root.values[attrVal] = Node(mCommonLabel, None)
    #         else:
    #             # Remove current best attribute from attributes dictionary
    #             newAttributes = attributes.copy()
    #             for attr in attributes:
    #                 if not attr == targetAttribute:
    #                     newAttributes[attr] = inputAttrs
    #                     # print(f'{TAG} newAttributes - {newAttributes}')
    #                     root.values[attrVal] = self.build_cont_tree(examplesVal, targetAttribute, newAttributes, attrsIndex)
    #     return root

    def build_cont_tree(self, trainingExamples, targetAttribute, attrsIndex, attrNames):
        #Generate candidate thresholds
        TAG = 'BUILD-CONT-TREE'
        labels = dataUtils.get_labels(trainingExamples)
        isPure, targetLabel = self.check_purity(labels)

        # print(f'{TAG} - attrVals {attrVals}')

        #Return if all examples are from the same class
        if isPure:
            return Node(targetLabel, None)
        #Generate continous attr values (thresholds)
        attrVals = dataUtils.get_cont_attrVals(attrNames, trainingExamples, labels)
        if not attrVals:
            # Return single-node tree root, with label = most common value of Target-attribute
            mCommonLabel = dataUtils.get_mcommon_label(labels)
            return Node(mCommonLabel, None)
        #Otherwise begin
        #Get the best attribute
        # bestAttr = dataUtils.find_best_attr(trainingExamples, attrNames, labels, attrsIndex)
        bestAttr = dataUtils.find_best_cont_attr(trainingExamples, attrVals, attrsIndex, attrNames)
        # print(f'{TAG} bestAttr - {bestAttr}')
        root = Node(bestAttr, ['Yes', 'No'])
        # print(f'{TAG} root - {root.attr}')
        # print(f'{TAG} root - {root.values}')
        #Get examples that meet the bestAttr threshold
        yesExamples = dataUtils.get_passing_training_examples(bestAttr, trainingExamples, attrsIndex)
        noExamples = dataUtils.get_non_passing_examples(bestAttr, trainingExamples, attrsIndex)

        if not yesExamples:
            mCommonLabel = dataUtils.get_mcommon_label(labels, attrNames[targetAttribute])
            root.values['Yes'] = Node(mCommonLabel, None)
        else:
            root.values['Yes'] = self.build_cont_tree(yesExamples, targetAttribute, attrsIndex, attrNames)
        
        if not noExamples:
            mCommonLabel = dataUtils.get_mcommon_label(labels, attrNames[targetAttribute])
            root.values['No'] = Node(mCommonLabel, None)
        else:
            root.values['No'] = self.build_cont_tree(noExamples, targetAttribute, attrsIndex, attrNames)
        return root


    def build_tree(self, trainingExamples, targetAttribute, attributes, attrsIndex):
        # # Create a root node
        # root = Node(None, None)
        TAG = 'BUILD-TREE'
        labels = dataUtils.get_labels(trainingExamples)
        # Check if attributes are continous. If they are: Do proper splitting and copy over all the other attrvalues. This is because continuous attributes must compete with all other attribtues
        # attributes = dataUtils.get_cont_attrVals(attributes, trainingExamples, labels, targetAttribute, attrsIndex)
        # print(f'{TAG} attributes - {attributes}')

        isPure, targetLabel = self.check_purity(labels)

        if self.verbose:
            print(f'Labels purity: {isPure},\ntargetLabel: {targetLabel}')

        if isPure:
            return Node(targetLabel, None)
        # print(f'BUILD-TREE: {attributes}')
        if not attributes:
            # Return single-node tree root, with label = most common value of Target-attribute
            mCommonLabel = dataUtils.get_mcommon_label(labels)
            return Node(mCommonLabel, None)

        # Begin main algorithm
        # Find attribute with highest info gain
        # TODO: Edit to accomodate thresholds
        bestAttr = dataUtils.find_best_attr(
            trainingExamples, attributes, labels, attrsIndex)
        
        # print(f'{TAG} bestAttr - {bestAttr}')

        root = Node(bestAttr, attributes[bestAttr])
        # #TODO: For a continous attribute, you would would all the attribute values from all the current attributes as branchces
        # # print(trainingExamples)

        for val in attributes[bestAttr]:
            # Get example subsets that have value = val
            examplesVal = dataUtils.get_val_examplesubsset(
                val, trainingExamples)
            # TODO: Make sure this works for continous values
            if not examplesVal:
                mCommonLabel = dataUtils.get_mcommon_label(labels, attributes[targetAttribute])
                root.values[val] = Node(mCommonLabel, None)
            else:
                # Remove the current best attribute because we already used it
                if self.verbose:
                    print(f'BUILD-TREE - attributes: {attributes}')
                    print(f'BUILD-TREE - bestAttr {bestAttr}')
                    print(f'BUILD-TREE - ***branch***: {val}')
                newAttributes = attributes.copy()
                del newAttributes[bestAttr]
                root.values[val] = self.build_tree(
                    examplesVal, targetAttribute, newAttributes, attrsIndex)
        return root

    def check_purity(self, labels):
        length = len(labels)
        # print(labels)
        targetLabel = labels[0]
        labelLen = 0
        for labl in labels:
            if labl == targetLabel:
                # print(f'{labl} == {targetLabel}')
                labelLen += 1
        return (labelLen == length), targetLabel
