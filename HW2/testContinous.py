from data_utils import DataUtils
from rules_utils import RulesUtils

dataUtils = DataUtils()
ruleUtils = RulesUtils()

class TestIris():
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def test(self, examples, rules, attrsIndex):
        TAG = 'TEST-IRIS'
        nCorrect = 0

        for example in examples:
            prediction = self.run_inference(example, rules, attrsIndex)
            if prediction == example[-1]:
                nCorrect += 1
            # print('-------------------------------------')
        return nCorrect/(len(examples))
    

    def run_inference(self, example, rules, attrsIndex):
        TAG = 'RUN-INFERENCE'
        for rule in rules:

            ruleExamples, prediction = ruleUtils.get_rule_examples([example], rule, attrsIndex) # Will return [example] if this rule satisfies the example, return [] otherwise
            if ruleExamples:
                return prediction
        return ''
        # Find rule that corresponds to this example