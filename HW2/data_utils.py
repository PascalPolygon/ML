import math
from multiprocessing.sharedctypes import Value
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

    def get_attr_values(self, examples, attr, attrsIndex):
        """
        Returns all the values from the training examples of the attribute attr
        """
        TAG = "GET-ATTR-VALS"
        vals = []
        # print(f'{TAG} attrsIndex - {attrsIndex}')
        c = attrsIndex[attr]
        for example in examples:
            vals.append(example[c])
        return vals

    def get_non_passing_examples(self, attrVal, examples, attrsIndex):
        _ , indices, _ = self.get_passing_cont_values(attrVal, examples, attrsIndex)
        nonPassingExamples = []
        # passingContVals, indices, vals
        for i, example in enumerate(examples):
            if not i in indices:
                nonPassingExamples.append(example)
        return nonPassingExamples

    def get_passing_training_examples(self, attrVal, examples, attrsIndex):
        TAG = 'GET-PASS-TRN-EXMPLES'
        # print(f'{TAG} examples - {len(examples)} {examples}')
        passingExamples , indices, _ = self.get_passing_cont_values(attrVal, examples, attrsIndex)
        # passingContVals, indices, vals
        passingTrainingExamples = []
        nonPassing = []
        # print(f'{TAG} attrVal - {attrVal}')
        # print(f'{TAG} passingIndices - {len(indices)}')
        # print(f'{TAG} passingExamples - {len(passingExamples)} {passingExamples}')
        for idx in indices:
            passingTrainingExamples.append(examples[idx])
        # for i, expl in enumerate(examples):
        #     if i in indices:
        #         continue
        #     else:
        #         nonPassing.append(expl)
        # print(f'{TAG} passingTrainingExamples - {len(passingTrainingExamples)}')
        # print(f'{TAG} nonPassing - {nonPassing}')
        return passingTrainingExamples


    def get_passing_cont_values(self, attrVal, examples, attrsIndex):
        TAG = 'GET-PASSING-CONT-VALS'
        # print(f'{TAG} attrVal - {attrVal}')
        attrValsElems = attrVal.split('-gt-')
        contAttr = attrValsElems[0]
        threshold = attrValsElems[1]
        # print(f'{TAG} attrVal - {attrVal}')
        # print(f'{TAG} contAttr - {contAttr}')
        # print(f'{TAG} threshold - {threshold}')
        vals = self.get_attr_values(examples, contAttr, attrsIndex)
        # print(f'{TAG} vals - {vals}')
        passingContVals = []
        indices = []
        for idx, val in enumerate(vals):
            if float(val) > float(threshold):
                passingContVals.append(val)
                indices.append(idx)
        # print(f'{TAG} vals (after threshold) - {passingContVals}')
        # print(f'{TAG} indices (after threshold) - {indices}')
        return passingContVals, indices, vals

    def calculate_cont_attr_ratios(self, contAttrVals, examples, attrsIndex):
        TAG = 'CALC_ATTR_RATIOS'
        ratios = []
        # vals - values 
        for attrVal in contAttrVals:
            passingContVals, _, vals = self.get_passing_cont_values(attrVal, examples, attrsIndex)
            # Get vals: all values in this column (petal-widht)
            ratios.append(len(passingContVals)/len(vals))
        return ratios


    def calculate_attr_ratios(self, examples, attributes, attr, attrsIndex, vals):
        """
        Returns the ratio for each attr val relative to all val of the attr
        Doesn't handle the case of having mixed attr values (threshold and descrete values  as attribute values for a continous attribute)
        """
        TAG = 'CALC_ATTR_RATIOS'
        ratios = []
        passingContVals = []
        # print(f'CALC_ATTR_RATIOS - attr: {attr}')
        # print(f'CALC_ATTR_RATIOS -  vals : {vals}')
        # print(f'{TAG} attr - {attr}')
        attrVals = attributes[attr]
        # print(uVals)
        # print(f'{TAG} attribute val length - {len(attrVals)}')
        for attrVal in attrVals:
            #For continous attributes, make sure the values satisfy the threshold
            if '-gt-' in attrVal:
                passingContVals, _ = self.get_passing_cont_values(attrVal, examples, attrsIndex)
                ratios.append(len(passingContVals)/len(vals))


                #TODO: Get the values from this contAttribute that satisfy the threshold
            else:
                #Does not handle mixed threshold and discrete attribute values/branches
                ratios.append(self.count1d(vals, attrVal)/len(vals))
                
        # print(f'{TAG} ratio length - {len(ratios)}')  
        # print(f'{TAG} ratios - {ratios}')
        # print('---------------------')
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
        """
        Returns -- for each target/label -- the ratio of examples that match attrVal
        """
        TAG = "CALC-TRGT-RATIOS"
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
    
    def calculate_cont_target_ratios(self, indices, targets, uTargets):
        """
        Returns -- for each target/label -- the ratio of examples that match attrVal
        For continous values, For each threshold conidition (attrVal) I want a list that will have len(uTargets) ratios)
        """
        nValues = len(indices)
        targetRatios = []

        for uTarget in uTargets:
            nLabels = 0
            for i, idx in enumerate(indices):
                if (targets[idx] == uTarget):
                    nLabels += 1
            targetRatios.append(nLabels/nValues)
        return targetRatios


    def find_cont_infogains(self, examples, contAttrVals, attrsIndex, attrNames):
        TAG = 'FIND-CONT-INFOGAINS'
        #Get attribute ratios: (For each candidate Threshold what is the % of data that passes this threshold)
        attrRatios = self.calculate_cont_attr_ratios(contAttrVals, examples, attrsIndex)
        # print(f'{TAG} attRatios ({len(attrRatios)}) - {attrRatios}')
        # print(f'{TAG} contAttrsVals ({len(contAttrVals)}) - ')
        attrTargetRatios = []
        targetAttr = list(attrNames)[-1]
        uTargets = attrNames[targetAttr]
        # print(f'{TAG} targetAttr - {targetAttr}')
        # print(f'{TAG} uTargets - {uTargets}')
        targets = self.get_labels(examples)
        # print(f'{TAG} targets - {targets}')
        for i, attrVal in enumerate(contAttrVals):
            _, indices, _ = self.get_passing_cont_values(attrVal, examples, attrsIndex)
            # print(f'{TAG} indices - {indices}')
            # print(f'{TAG} attrRatio - {attrRatios[i]}')
            if not indices:
                attrTargetRatios.append([])
            else:
                targetRatios = self.calculate_cont_target_ratios(indices, targets, uTargets)
                attrTargetRatios.append(targetRatios)
        # print(f'{TAG} attrTargetRatios - {attrTargetRatios}')
        gains = []
        for i, attrRatio in enumerate(attrRatios):
                # print(attrTargetRatios[i])
            if attrRatio > 0:
                gains.append(attrRatio * \
                    self.calculate_entropy(attrTargetRatios[i]))
            else:
                gains.append(1000000) #Super high gain for attrRatios that are zero
        return gains
        

    def find_highest_infogain(self, examples, attributes, targets, attrsIndex):
        # print(attributes)
        # uTargets = attributes[attributes[-1]]
        TAG = "FIND-HIGST-INFOGAIN"
        targetAttr = list(attributes)[-1]
        uTargets = attributes[targetAttr]
        # print(f'HIGHEST-INFO-GAIN - uTargets: {uTargets}')
        gains = []
        isContData = False

        for attr in attributes:
            # print(attr)
            if attr is not targetAttr:  # Only for non target attributes
                attrGain = 0
                vals = self.get_attr_values(
                    examples, attr, attrsIndex) #Return the data column for this attribute
                # print(f'{TAG} - attr - {attr}')
                # print(f'{TAG} - vals - {vals}')
                attrRatios = self.calculate_attr_ratios(
                    examples, attributes, attr, attrsIndex, vals)
                # print(f'{TAG} attrRatios - {attrRatios}')

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
                    # print(f'HIGHEST-INFO-GAIN - length of vals: {len(vals)}')
                    # print(f'HIGHEST-INFO-GAIN - attrVal: {attrVal}')
                    # For continous values, For each threshold conidition (attrVal) I want a list that will have 3 elements(1/unique target label)
                    if '-gt-' in attrVal:
                        isContData = True
                        anyContAttr = attr
                        # Continous values. Get teh values for this attrVal
                        # For continous values, For each threshold conidition (attrVal) I want a list that will have len(uTargets) ratios)
                        # print(f'{TAG} attrVal - {attrVal}')
                        # print(f'{TAG} examples - {examples}')
                        _, indices = self.get_passing_cont_values(attrVal, examples, attrsIndex)
                        # self.calculate_cont_target_ratios
                        targetRatios = self.calculate_cont_target_ratios(indices, targets, uTargets)
                        attrTargetRatios.append(targetRatios)
                        # print(f'{TAG} targetRatios - {attrVal} : {targetRatios}')
                        # attrValsElems = attrVal.split('-gt-')
                        # contAttr = attrValsElems[0]
                        # threshold = attrValsElems[1]
                        # vals = self.get_attr_values(examples, contAttr, attrsIndex)
                        # passingContVals, _ = self.get_passing_cont_values(threshold, vals)
                    else: 
                        if attrVal in vals:
                            # TODO: modify to accomodate continous values and thresholds
                            targetRatios = self.calculate_target_ratios(
                                attrVal, vals, targets, uTargets)
                            attrTargetRatios.append(targetRatios)

                # print(f'HIGHEST-INFO-GAIN - attrTargetRatios: {len(attrTargetRatios)}')
                # print(f'HIGHEST-INFO-GAIN - attrRatios: {len(attrRatios)}')
                
                if not isContData:
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
                

        if isContData:
            print('Coutinous data')
            # print(f'HIGHEST-INFO-GAIN - attrTargetRatios: {(attrTargetRatios)}')
            # print(f'HIGHEST-INFO-GAIN - attrRatios: {(attrRatios)}')
            candidateThresholds = attributes[anyContAttr]
            # print(attributes[anyContAttr])
            for i, attrRatio in enumerate(attrRatios):
                    # print(attrTargetRatios[i])
                if attrRatio > 0:
                    gains.append(attrRatio * \
                        self.calculate_entropy(attrTargetRatios[i]))
            return gains, candidateThresholds

            # for attV

        return gains, None

    def find_best_cont_attr(self, examples, contAttrVals, attrsIndex, attrNames):
        TAG = 'FIND-BEST-CON-ATTR'
        # print(f'{TAG} contAttrVals ({len(contAttrVals)}) - {contAttrVals}')
        # print(f'{TAG} examples - {examples}')
        gains = self.find_cont_infogains(examples, contAttrVals, attrsIndex, attrNames)
        # print(f'{TAG} gains ({len(gains)}) - {gains}')
        bestAttr = contAttrVals[gains.index(min(gains))]  # Minimum value of this gain corresponds to highest information gain
        return bestAttr
        # self.find_highest_infogain(examples, contAttrVals)
        # gains, candidateThresholds = self.find_highest_infogain(examples, attributes, labels, attrsIndex)

    def find_best_attr(self, examples, attributes, labels, attrsIndex):
        # if self.verbose:
        #     print(examples)
        TAG = 'FIND-BEST-ATTR'
        inputAttrs = list(attributes)[:-1]
        targetAttr = list(attributes)[-1]
        # print(f'{TAG} inputAttrs - {inputAttrs}')
        # vals = self.get_attr_values(
        #     examples, targetAttr, attrsIndex) #Get values of target attribute
        # TODO: We don't need entropy to calculate the highest Info gain 
        # ratios = self.calculate_attr_ratios(
        #     examples, attributes, targetAttr, attrsIndex, vals) #Ratios of target attribute used to calculate entropy of entire dataset
        # # print(ratios)
        # entropy = self.calculate_entropy(ratios) #Calculate the entropy of the entire data
        #TODO: make sure this can accomodate continuous attributes
        gains, candidateThresholds = self.find_highest_infogain(examples, attributes, labels, attrsIndex)
        # print(f'{TAG} gains - {gains}')
        # print(f'{TAG} candidateThresholds - {candidateThresholds}')
        if candidateThresholds is not None:
            #Continuous data
            bestAttr = candidateThresholds[gains.index(min(gains))]  # Minimum value of this gain corresponds to highest information gain
        else:
             # Minimum value of this gain corresponds to highest information gain
            bestAttr = inputAttrs[gains.index(min(gains))]
       
        # print(f'Ratios: {ratios}')
        # print(f'Entropy: {entropy}')
        # print(f'Gains: {gains}')
        if self.verbose:
            print(f'Ratios: {ratios}')
            print(f'Entropy: {entropy}')
            print(f'Gains: {gains}')
        return bestAttr

    
    def get_cont_attrVals(self, attrs, trainingExamples, labels):
        TAG = "GET-CONT-ATTRVALS"
        # print(f'{TAG} pre inputAttrs - {attrs}')
        contAttrVals = [] #Continus attribute values
        # contAttrs = []

        for i, key in enumerate(attrs):
            if attrs[key][0] == 'continuous':
                # contAttrs.append(key) #Store keys of continuous attributes so we know who they are later. 
                attrVals = self.get_column(trainingExamples, i)
                sortedAttrVals = attrVals.copy()
                sortedLabels = [x for _,x in sorted(zip(sortedAttrVals,labels))]
                sortedAttrVals.sort()
                thresholds = self.find_thresholds(sortedAttrVals, sortedLabels)
                # print(f'{TAG} thresholds - {thresholds}')

                for thrsh in thresholds:
                    contAttrVals.append(f'{key}-gt-{thrsh}')
        # print(f'{TAG} with duplicates: {len(contAttrVals)}')
        # contAttrVals = list(set(contAttrVals)) #Dirty hack to avoid duplicates
        # print(f'{TAG} without duplicates: {len(contAttrVals)}')
        return contAttrVals

    def get_column(self, examples, c):
        col = []
        for example in examples:
            col.append(float(example[c]))
        return col

    #Duplicates
    # def find_thresholds(self, vals, labels):
    #     currentLabel = labels[0]
    #     thresholds = []
    #     for i, labl in enumerate(labels):
    #         if currentLabel != labl: #Adjacent examples with different classfication
    #             currentLabel = labl
    #             # print(f'Change between idx {i-1} and {i}')
    #             thresholds.append((vals[i-1] + vals[i])/2)
    #     return thresholds

    #Less duplicates
    def find_thresholds(self, vals, labels):
        # currentLabel = labels[0]
        thresholds = []
        i = 0
        while i < len(labels)-1:
            if labels[i] != labels[i+1]:
                thresholds.append((vals[i] + vals[i+1])/2)
                i += 2 #Skip the next one (vals[i+1]) cause we aleady used it to find a threshoold
            else:
                i+=1
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

    def get_mcommon_label(self, labels, uTargets):
        TAG = 'GET-MOST-CMMN-LABL'
        print(f'{TAG} uTargets - {uTargets}')
        counts = []
        for uTarget in uTargets:
            counts.append(self.count1d(labels, uTarget))
        maxIdx = counts.index(max(counts))
        return uTargets[maxIdx]
        # print(f'{TAG} label - {len(labels)}')

    # def print_tree(self, tree, level=0):
    #     if tree == None:
    #         return
    #     if tree.values:
    #         for i, val in enumerate(tree.values):
    #             if tree.values[val] is not None:
    #                 valuesList = list(tree.values[val].values.items())
    #                 if valuesList:  # Not a leaf node
    #                     print('|\t' * level + str(tree.attr) + ' = ' + val)
    #                     self.print_tree(tree.values[val], level+1)
    #                 else:  # This is a leaf node
    #                     print('|\t' * level + str(tree.attr) + ' = ' +
    #                         val + ' : ' + tree.values[val].attr)
    #     else:
    #         print('|\t' * level + str(tree.attr))

    def print_tree(self, tree, level=0):
        if tree == None:
            return
        if tree.values:
            for i, val in enumerate(tree.values):
                if tree.values[val] is not None:
                    valuesList = list(tree.values[val].values.items())
                    if valuesList:  # Not a leaf node
                        print('| ' * level + str(tree.attr) + ' = ' + val)
                        self.print_tree(tree.values[val], level+1)
                    else:  # This is a leaf node
                        print('| ' * level + str(tree.attr) + ' = ' +
                            val + ' : ' + tree.values[val].attr)
        else:
            print('| ' * level + str(tree.attr))