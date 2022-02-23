from attr import attrs
from data_utils import DataUtils

dataUtils = DataUtils()

class RulesUtils:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def test_rule_acc(self, examples, rule, attrsIndex):
        TAG = 'TEST-RULE-ACC'
        ruleExamples, prediction = self.get_rule_examples(examples, rule, attrsIndex)
        if ruleExamples:
            nCorrect = 0
            for ruleExample in ruleExamples:
                target = ruleExample[-1]
                # print(f'{TAG} target - {target}')
                if target == prediction:
                    nCorrect += 1
            return nCorrect/len(ruleExamples)
        else:
            # This rule doesn't match any examples
            # We can't determine the accuracy of this rule
            return None

    def get_rule_examples(self, examples, rule, attrsIndex):
            """
            Takes in a list of examples, and one rule from the rules set
            Returns the susbset of examples that satisify the rule
            """
            TAG = 'GET-RULE-EXAMPLES'
            antecedants = rule.split('^')
            antecedant = antecedants[0]
            #Remove this antecedant from antecedants because we already used it 
            del antecedants[0]
            rule = '^'.join(antecedants) #new rule without used antecedant
            condition = antecedant.split('=')
            if condition[1].strip() == 'Yes':
                # print('Passing')
                newExamples = dataUtils.get_passing_training_examples(condition[0].strip(), examples, attrsIndex)
            else:
                # print('Non-passing')
                newExamples = dataUtils.get_non_passing_examples(condition[0].strip(), examples, attrsIndex)
            anteElements = antecedant.split('-gt-')
            if '=>' in anteElements[1]:
                #This is the last precondition and the consequent
                prediction = anteElements[1].split('=>')[1].strip()
                return newExamples, prediction
            else:
                return self.get_rule_examples(newExamples, rule, attrsIndex)

    def prune_rule(self, rule, examples, prevAcc, attrsIndex):
        TAG = 'PRUNE-RULE'
        if prevAcc < 1.0:
            antecedants = rule.split('^')
            if len(antecedants) < 2:
                return rule
            antecedantsCopy = antecedants.copy()
            for antecedant in antecedants:
                del antecedantsCopy[antecedantsCopy.index(antecedant)]
                newRule = '^'.join(antecedantsCopy) #new rule without pruned antecedant
                # print(f'{TAG} newRule - {newRule}')
                newAcc = self.test_rule_acc(examples, newRule, attrsIndex)
                # print(f'{TAG} newAcc - {newAcc}')
                if newAcc > prevAcc:
                    #Further prune
                    return newRule
                    # return self.prune_rule(newRule, examples, newAcc, attrsIndex)
                else:
                    return self.prune_rule(newRule, examples, newAcc, attrsIndex)
        else:
            #Don't prune this rule, just return it
            return rule

        # Remove first antecedant, test rule acc, if rule acc is better then orriginal futher prune, otherwise prune the next one