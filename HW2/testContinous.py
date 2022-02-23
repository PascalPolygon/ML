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
            # print(f'{TAG} prediction - {prediction}')
            # print(f'{TAG} target - {example[-1]}')
            if prediction == example[-1]:
                nCorrect += 1
            # print('-------------------------------------')
        return nCorrect/(len(examples))
        # for example in examples:
        #     self.run_inference(example, rules, attrsIndex)
    

    def run_inference(self, example, rules, attrsIndex):
        TAG = 'RUN-INFERENCE'
        # print(f'{TAG} example - {example}')
        # print(f'{TAG} rules - {rules}')
        # print([example])
        #Start with the rule check each antecedant one at a time
        # ruleUtils.get_antecedants(rule)
        for rule in rules:

            ruleExamples, prediction = ruleUtils.get_rule_examples([example], rule, attrsIndex) # Will return [example] if this rule satisfies the example, return [] otherwise
            if ruleExamples:
                # print(f'{TAG} example - {example}')
                # print(f'{TAG} rule - {rule}')
                # print(f'{TAG} ruleExamples - {ruleExamples}')
                # print(f'{TAG} rulePrediction - {prediction}')
                return prediction
        return ''
        # Find rule that corresponds to this example