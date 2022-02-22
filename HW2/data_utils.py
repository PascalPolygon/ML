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

    def get_passing_training_examples(self, attrVal, examples, attrsIndex):
        TAG = 'GET-PASS-TRN-EXMPLES'
        # print(f'{TAG} examples - {len(examples)} {examples}')
        passingExamples , indices = self.get_passing_cont_values(attrVal, examples, attrsIndex)
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
        return passingContVals, indices

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
            # print(f'{TAG}  attrVal - {attrVal}')
            if '-gt-' in attrVal:
                #This is a thresold attribute value for a continous attribute
                # make sure the values satisfy the threshold
                
                #Doesn't handle the case of having mixed attr values (threshold and descrete values  as attribute values for a continous attribute)
                #Get the name of the attribute
                passingContVals, _ = self.get_passing_cont_values(attrVal, examples, attrsIndex)
                # attrValsElems = attrVal.split('-gt-')
                # contAttr = attrValsElems[0]
                # threshold = attrValsElems[1]
                # vals = self.get_attr_values(examples, contAttr, attrsIndex)
                # passingContVals, _ = self.get_passing_cont_values(threshold, vals)
                # print(f'{TAG} passingContVals - {passingContVals}')
                # print(f'{TAG} lenght of vals - {len(vals)}')
                # print(f'{TAG} lenght of passingContVals - {len(passingContVals)}')
                ratios.append(len(passingContVals)/len(vals))
                # print(f'{TAG} ratio length - {len(ratios)}')
                # #Get values of continues attribute
                # vals = self.get_attr_values(examples, contAttr, attrsIndex)
                # print(f'{TAG} {contAttr} vals - {vals}')
                # #Check threshold
                # for val in vals:
                #     if float(val) > float(threshold):
                #         passingContVals.append(val)


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

    def find_best_attr(self, examples, attributes, labels, attrsIndex):
        # if self.verbose:
        #     print(examples)
        TAG = 'FIND-BEST-ATTR'
        inputAttrs = list(attributes)[:-1]
        targetAttr = list(attributes)[-1]
        print(f'{TAG} inputAttrs - {inputAttrs}')
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
            bestAttr = candidateThresholds[gains.index(min(gains))]
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

    def get_cont_attrVals(self, attrs, trainingExamples, labels, targetAttr, attrsIndex):
        TAG = "GET-CONT-ATTRVALS"
        # print(f'{TAG} pre inputAttrs - {attrs}')
        contAttrVals = [] #Continus attribute values
        contAttrs = []
        nonContAttrs = []

        for i, key in enumerate(attrs):
            # print(f'{TAG} - {key} = {attrs[key][0]}')
            print(f'{TAG} attrVal - {attrs[key]}')
            if attrs[key][0] == 'continuous':
                contAttrs.append(key) #Store keys of continuous attributes so we know who they are later. 
                # print(f'{TAG} {key} Corresponding col in data: {i}')
                #Get the corresponding data from inputExamples
                attrVals = self.get_column(trainingExamples, i)
                # attrVals = self.get_attr_values(trainingExamples, key, attrsIndex)
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
        print(f'{TAG} with duplicates: {len(allAttrVals)}')
        allAttrVals = list(set(allAttrVals)) #Dirty hack to avoid duplicates
        print(f'{TAG} without duplicates: {len(allAttrVals)}')
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

    def get_mcommon_label(self, labels, uTargets):
        TAG = 'GET-MOST-CMMN-LABL'
        print(f'{TAG} uTargets - {uTargets}')
        counts = []
        for uTarget in uTargets:
            counts.append(self.count1d(labels, uTarget))
        maxIdx = counts.index(max(counts))
        return uTargets[maxIdx]
        # print(f'{TAG} label - {len(labels)}')

