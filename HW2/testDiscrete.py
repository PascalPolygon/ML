from data_utils import DataUtils

data_utils = DataUtils()
class TestTennis():
    def __init__(self, verbose=False):
        self.data = []
        self.verbose = verbose

    def test(self, root, data, attrsIndex):
        TAG = 'TEST'
        # print(f'{TAG} Print tree - ')
        # data_utils.print_tree(root)
        # print(f'{TAG} testData - {data}')
        predictions = []
        for example in data:
            # Run the example through the tree and get the classification
            inputs = example[:-1]
            # print(f'{TAG} inputs - {inputs}')
            prediction = self.run_tree_inference(root, inputs, attrsIndex)
            # print(f'{TAG} prediction {prediction}')
            predictions.append(prediction)
            if self.verbose:
                print(f'{TAG} inputs - {inputs}')
                print(f'{TAG} prediction {prediction}')

        
        nSamples = len(data)
        nCorrectPred = 0
        for pred, example in zip(predictions, data):
            # Get true target
            target = example[-1]
           
            if pred == target:
                nCorrectPred += 1

            if self.verbose:
                print(f'{TAG} prediction - {pred}, target - {target}')
        return nCorrectPred/nSamples #Accuracy



        # Calculate and return accuracy


    def run_tree_inference(self, root, inputData, attrsIndex):
        TAG = 'RUN-TREE-INF'
        # print(f'{TAG} attrsIndex - {attrsIndex}')
        firstAttr = root.attr
        if firstAttr == 'Yes' or firstAttr == 'No':
            # print(f'{TAG} returning {firstAttr}')
            return firstAttr
        # print(f'{TAG} firstAttr - {firstAttr}')
        firstAttrIndex = attrsIndex[firstAttr]
        attrVal = inputData[firstAttrIndex]
        # print(f'{TAG} Going down {attrVal} branch') #Go down this branch
        return self.run_tree_inference(root.values[attrVal], inputData, attrsIndex)
