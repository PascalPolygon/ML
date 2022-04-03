import random
from utils import Utils

utils = Utils()

class Gabil:
    def __init__(self, verbose=False):
        self.data = []
        self.verbose=verbose
    
    def generate_tennis_rule(self):
        rule = []
        for _ in range(11):
            rule.append(1 if random.random() > 0.5 else 0)
        if self.verbose:
            utils.log('Random rule', rule)
        return rule 
    
    def generate_hypotheses(self, rules):
        H = []
        used_rules = []
        # for rule in rules:
        i = 0
        while len(used_rules) < len(rules):
            rule_id = random.randint(0, len(rules)-1)

            if i == 0:
                rule = rules[rule_id]
                H.append(rule)
                used_rules.append(rule_id)
                if self.verbose:
                    utils.log(f'using rule {[rule_id]}', rule)
            else:
                if not rule_id in used_rules:
                    used_rules.append(rule_id)
                    rule = rules[rule_id]
                    if self.verbose:
                        utils.log(f'using rule {[rule_id]}', rule)
                    #Determine if rule_id should be concat to existing hypo or make a new hypothesis
                    d = random.randint(0, len(H))

                    if d <= len(H)-1:
                        # temp = H[d]
                        H[d] += rules[rule_id] #Contatenate to existing rule set
                    else:
                        H.append(rules[rule_id]) #Create a new rule set
                    # utils.log('rule_id', rule_id)
                    # utils.log('rule', rules[rule_id])
            i+=1
        utils.log('used_rules', used_rules)
        # utils.log('H', H)
        return H


    def tennis(self, fit_thres, q, p, r, m):
        #Generate q random rulues
        #33221
        #Outlook(3), Temperature(3), Humidity(2), Wind(2), PlayTennis(1)
        rules = []
        for _ in range(q):
            rules.append(self.generate_tennis_rule())
        print('-'*20)
        H = self.generate_hypotheses(rules)

        if self.verbose:
            print('-'*20)
            for i, h in enumerate(H):
                utils.log(f'h{i} {len(h)}', h)
        
        #Evluate fitness of each hypothesis in H
            # utils.log('random rule', rule)
        #Create p hypotheses from q random rules
