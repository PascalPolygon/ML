import math
from re import T


class DataUtils():
    def __init__(self, verbose=False):
        # self.data = []
        self.verbose = verbose

    def count1d(self, r, val):
        return sum(x == val for x in r)

    def get_labels(self, examples):
        labels = []
        for example in examples:
            labels.append(example[-1])
        return labels

    def get_unique_labels(self, labels):
        uniqueLabels = []
        for labl in labels:
            if not labl in uniqueLabels:
                uniqueLabels.append(labl)
        return uniqueLabels

    # def get_attr_ratios(self, vals, uVals):
    #     ratios = []
    #     for uVal in uVals:
    #         ratios.append(self.count1d(vals, uVals)/len(vals))
    #     return ratios

    def get_attr_values(self, examples, attributes, attr, attrsIndex):
        vals = []
        # print(f'GET_ATTR_VALUES - attributes: {attributes}')
        # print(f'GET_ATTR_VALUES - attr: {attr}')
        c = attrsIndex[attr]
        # print(f'GET_ATTR_VALUE - c: {c}')
        for example in examples:
            # print(f'GET_ATTR_VALUES - example: {example}')
            vals.append(example[c])
        return vals

    def calculate_attr_ratios(self, examples, attributes, attr, attrIndex, vals):
        ratios = []
        # print(f'CALC_ATTR_RATIOS - attr: {attr}')
        # print(f'CALC_ATTR_RATIOS -  vals : {vals}')
        uVals = attributes[attr]
        # print(uVals)
        for uVal in uVals:
            ratios.append(self.count1d(vals, uVal)/len(vals))
        return ratios

    def calculate_entropy(self, ratios):
        entropy = 0
        for p in ratios:
            if p == 0:
                continue  # This term will be zero so we can just skip it
            else:
                entropy += p*math.log(p, 2)
        return -1*entropy

    def calculate_target_ratios(self, attrVal, values, targets, uTargets):
        targetRatios = []

        # print(values)
        # print(attrVal)
        nValues = self.count1d(values, attrVal)
        # uLabels = attributes[attributes[-1]]
        for uTarget in uTargets:
            nLabels = 0
            for i, target in enumerate(targets):
                if values[i] == attrVal and target == uTarget:
                    nLabels += 1
            targetRatios.append(nLabels/nValues)
        return targetRatios

        # Append here

        for i, val in enumerate(values):
            if val == attrVal:
                targets

    def find_highest_infogain(self, entropy, examples, attributes, targets, attrsIndex):
        # print(attributes)
        # uTargets = attributes[attributes[-1]]
        targetAttr = list(attributes)[-1]
        uTargets = attributes[targetAttr]
        # print(f'HIGHEST-INFO-GAIN - uTargets: {uTargets}')
        gains = []

        for attr in attributes:
            # print(attr)
            if attr is not targetAttr:  # Only for non target attributes
                attrGain = 0
                vals = self.get_attr_values(
                    examples, attributes, attr, attrsIndex)
                attrRatios = self.calculate_attr_ratios(
                    examples, attributes, attr, attrsIndex, vals)

                try:
                    rmIdx = attrRatios.index(0.0)
                    # Remove attribute ratios that are zero: means they are not par to the example subset
                    del attrRatios[rmIdx]
                    # print(f'HIGHEST-INFO-GAIN - rmIdx: {rmIdx}')
                except ValueError:
                    if self.verbose:
                        print(f'[WARNING] 0.0 is not in list')
                # attrVals = attributes[attr]
                attrTargetRatios = []
                for attrVal in attributes[attr]:
                    # print(attrVal)
                    # print(f'HIGHEST-INFO-GAIN - vals: {vals}')
                    if attrVal in vals:
                        targetRatios = self.calculate_target_ratios(
                            attrVal, vals, targets, uTargets)
                        attrTargetRatios.append(targetRatios)

                # print(f'HIGHEST-INFO-GAIN - attrVals: {attributes[attr]}')
                # print(f'HIGHEST-INFO-GAIN - attrRatios: {attrRatios}')
                for i, attrRatio in enumerate(attrRatios):
                    # print(attrTargetRatios[i])
                    if attrRatio > 0:
                        # print(f'HIGHEST-INFO-GAIN - i : {i}')
                        # print(
                        #     f'HIGHEST-INFO-GAIN - attrTargetRatios : {attrTargetRatios}')
                        attrGain += attrRatio * \
                            self.calculate_entropy(attrTargetRatios[i])

                # print(f'Gain for {attr} = {attrGain}')
                gains.append(attrGain)
        return gains

    def find_best_attr(self, examples, attributes, labels, attrsIndex):
        # if self.verbose:
        #     print(examples)
        inputAttrs = list(attributes)[:-1]
        targetAttr = list(attributes)[-1]

        vals = self.get_attr_values(
            examples, attributes, targetAttr, attrsIndex)

        ratios = self.calculate_attr_ratios(
            examples, attributes, targetAttr, attrsIndex, vals)
        # print(ratios)
        entropy = self.calculate_entropy(ratios)
        gains = self.find_highest_infogain(
            entropy, examples, attributes, labels, attrsIndex)
        # Minimum value of this gain corresponds to highest information gain
        bestAttr = inputAttrs[gains.index(min(gains))]
        if self.verbose:
            print(f'Ratios: {ratios}')
            print(f'Entropy: {entropy}')
            print(f'Gains: {gains}')
        return bestAttr

    def get_cont_attrVals(self, attrs, trainingExamples, labels, targetAttr):
        TAG = "GET-CONT-ATTRVALS"
        print(f'{TAG} pre inputAttrs - {attrs}')
        contAttrVals = [] #Continus attribute values
        contAttrs = []
        nonContAttrs = []

        for i, key in enumerate(attrs):
            # print(f'{TAG} - {key} = {attrs[key][0]}')
            if attrs[key][0] == 'continuous':
                contAttrs.append(key) #Store keys of continuous attributes so we know who they are later. 
                # print(f'{TAG} {key} Corresponding col in data: {i}')
                #Get the corresponding data from inputExamples
                attrVals = self.get_column(trainingExamples, i)
                sortedAttrVals = attrVals.copy()
                sortedLabels = [x for _,x in sorted(zip(sortedAttrVals,labels))]
                #Find where 
                # print(sortedAttrVals)
                #Sort attrVals and crate threshold
                sortedAttrVals.sort()
                thresholds = self.find_thresholds(sortedAttrVals, sortedLabels)

                for thrsh in thresholds:
                    contAttrVals.append(f'{key}-gt-{thrsh}')
            else:
                #Get attribute values of non-continous attributes
                #Make sure this is not the target (target Attribute)
                if not key == targetAttr:
                    for attrVal in attrs[key]:
                        nonContAttrs.append(attrVal)
        
        
        allAttrVals = contAttrVals + nonContAttrs #also add atributes of discrete variables
        # print(f'{TAG} allAttrsVals -  {allAttrVals}')
        for contAttr in contAttrs:
            attrs[contAttr] = allAttrVals #Edit input attribute objects with newly calculate thresholds for continous attributes
        return attrs

    def get_column(self, examples, c):
        col = []
        for example in examples:
            col.append(float(example[c]))
        return col

    def find_thresholds(self, vals, labels):
        currentLabel = labels[0]
        thresholds = []
        for i, labl in enumerate(labels):
            if currentLabel != labl: #Adjacent examples with different classfication
                currentLabel = labl
                # print(f'Change between idx {i-1} and {i}')
                thresholds.append((vals[i-1] + vals[i])/2)
        return thresholds
        
    def get_input_examples(self, examples):
        newExamples = []
        for example in examples:
            newExamples.append(example[:-1]) #Do not keep classification
        return newExamples


    def get_val_examplesubsset(self, val, examples):
        newExamples = []
        for example in examples:
            if val in example:
                newExamples.append(example)
        return newExamples
