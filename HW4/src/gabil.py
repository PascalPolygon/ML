import random
from re import S
# from xml.sax.xmlreader import InputSource
from utils import Utils
import math
import copy

utils = Utils()

class Gabil:
    def __init__(self, inputs, targets, verbose=False):
        self.data = []
        self.inputs = inputs
        self.targets = targets
        self.verbose=verbose
    
    def generate_tennis_rule(self):
        rule = []
        for _ in range(11):
            rule.append(1 if random.random() > 0.5 else 0)
        # if self.verbose:
        #     utils.log('Random rule', rule)
        return rule 

    def match_substring(self, example_substring, rule_substring):
        pos_ids = []
        #Get indices of bit in example that are positive
        for i, bit in enumerate(example_substring):
            if bit == 1:
                pos_ids.append(i)
        # utils.log('pos_ids', pos_ids)
        nBitMatches = 0
        #Check that those same indices are positive in the rule (We don't care about negative bits in the example)
        for id in pos_ids:
            if rule_substring[id] == 1:
                nBitMatches += 1
        if nBitMatches == len(pos_ids):
            # utils.log('precondition matches rule')
            return 1
        else:
            return 0
        # print('-'*20)

    def test_rule(self, rule):
        nCorrect = 0
        for input, target in zip(self.inputs, self.targets):
            outlook_example = input[:3]
            outlook_rule = rule[:3]

            temp_example = input[3:6]
            temp_rule = rule[3:6]

            hum_example = input[6:8]
            hum_rule = rule[6:8]

            wind_example = input[8:10]
            wind_rule = rule[8:10]

            pred = rule[10]
            # outlook_rule = [1,0,1]
            res = 0
            # utils.log('Matching outlook (sample | rule)', f'{outlook_example} | {outlook_rule}')
            res += self.match_substring(outlook_example, outlook_rule)
            res += self.match_substring(temp_example, temp_rule)
            res += self.match_substring(hum_example, hum_rule)
            res += self.match_substring(wind_example, wind_rule)

            if res == 4:
                pred = [pred]
                if pred == target:
                    nCorrect += 1
                    # if self.verbose:
                    #     utils.log(f'Rule {rule} classifies examples {input+target}')
        return nCorrect

    
        #Match temperature
        #Match humidity
        #Match wind
        #Match playtennis

    def correct(self, h):
        #Extract individual rules from hypothesis
        rule = []
        nCorrect = 0 #n examples correctly classified by this hypothesis
        for bit in h:
            rule.append(bit)
            if len(rule) == 11:
                nCorrect += self.test_rule(rule)
                rule = []
        return nCorrect


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
                # if self.verbose:
                #     utils.log(f'using rule {[rule_id]}', rule)
            else:
                if not rule_id in used_rules:
                    used_rules.append(rule_id)
                    rule = rules[rule_id]
                    # if self.verbose:
                    #     utils.log(f'using rule {[rule_id]}', rule)
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
        # utils.log('used_rules', used_rules)
        # utils.log('H', H)
        return H

    def select(self, n, P, fitnessCopy, fitnessSum):
            nLoop = 0
            selected = []
            while len(selected) < n:
                if nLoop == 70:
                    utils.log('[Bad start!] Likely due to not enough fit individuals, restarting...')
                    return None, True
                
                for i, f in enumerate(fitnessCopy):
                    pr = f/fitnessSum
                    # utils.log('fitness', fitnessCopy)
                    # utils.log(f'hypo {i} pr = {pr}')
                    prob_thresh = random.random()
                    # utils.log(f'Prob thresh {prob_thresh}')

                    if prob_thresh <= pr:
                        # utils.log(f'Keeping {Pcopy[i]}')
                        selected.append(P[i])
                        fitnessCopy[i] = -1 #Assign bad fitness to used hypotheses so they are not reused

                        if len(selected) == n:
                            break
                nLoop += 1
            return selected, False

    def selectEager(self, n, P, fitnessCopy):
            nLoop = 0
            selected = []
            selected_ids = []

            while len(selected) < n:
                if nLoop == 70:
                    utils.log('[Bad start!] Likely due to not enough fit individuals, restarting...')
                    return None, True
                
                fitnessSum = sum(fitnessCopy)

                if fitnessSum == 0:
                    #Select a hypothesis at random
                    random_selectable = []
                    for i in range(len(fitnessCopy)):
                        if not i in selected_ids:
                            random_selectable.append(i)
                    random_select = random.choice(random_selectable)
                    utils.log(f'Randomly selected h[{random_select}]')
                    selected_ids.append(random_select)
                    selected.append(P[random_select])
                    if len(selected) == n:
                            break
                else:
                    for i, f in enumerate(fitnessCopy):
                        pr = f/fitnessSum
                        # utils.log('fitness', fitnessCopy)
                        # utils.log(f'hypo {i} pr = {pr}')
                        prob_thresh = random.random()
                        # utils.log(f'Prob thresh {prob_thresh}')

                        if prob_thresh <= pr:
                            # utils.log(f'Keeping {Pcopy[i]}')
                            selected_ids.append(i)
                            selected.append(P[i])
                            fitnessCopy[i] = 0 #Assign bad fitness to used hypotheses so they are not reused

                            if len(selected) == n:
                                break
                nLoop += 1
            return selected, False
    
    def calculate_d1(self, boundaries, p1):
        for i in range(len(boundaries)-1, -1, -1):
            # print(i)
            if p1 > boundaries[i]:
                d1 = p1 - boundaries[i]
                return d1

    def calculate_d2(self, boundaries, p2):
        for i in range(len(boundaries)-1, -1, -1):
            if boundaries[i] < p2:
                d2 = p2 - boundaries[i]
                return d2

    def crossover(self, h1, h2, l=5):
        p1 = p2 = 0
        # h2 = [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]+[1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]
        h1 = [1,0,0,1,1,1,1,1,0,0]
        h2 = [0,1,1,1,0,1,0,0,1,0]
        while not p1 < p2:
            p1 = random.randint(0, len(h1)-2)
            p2 = random.randint(p1, len(h1)-1)
            p1 =0
            p2 = 7
        # rule_boundaries = []
        utils.log('p1', p1)
        utils.log('p2', p2)
        nBoundaries = int(len(h1)/l)
        boundaries = [(i*l)-1 if i > 0 else (i*l) for i in range(nBoundaries)]
        # boundaries[1:] -=1
        utils.log('boundaries h1', boundaries)

        # for i in range(len(boundaries)):
        #     if boundaries[i] > p1:
        #         d1 = p1 - boundaries[i-1]
        d1 = self.calculate_d1(boundaries, p1)
        d2 = self.calculate_d2(boundaries, p2)
        # for i in range(len(boundaries)-1, -1, -1):
        #     # print(i)
        #     if p1 > boundaries[i]:
        #         d1 = p1 - boundaries[i]
        #         break
        # for i in range(len(boundaries)-1, -1, -1):
        #     if boundaries[i] < p2:
        #         d2 = p2 - boundaries[i]
        #         break
        utils.log('d1', d1)
        utils.log('d2', d2)
        #parent 2 boundaries
        nBoundaries = int(len(h2)/l)
        boundaries = [(i*l)-1 if i > 0 else (i*l) for i in range(nBoundaries)]
        utils.log('boundaries h2', boundaries)
        p1_list = []
        p2_list = []
        for i in range(len(h2)):
            test_d1 = self.calculate_d1(boundaries, i)
            test_d2 = self.calculate_d2(boundaries, i)
            if test_d1 == d1:
                p1_list.append(i)
            if test_d2 == d2:
                p2_list.append(i)

        utils.log('p1_list', p1_list)
        utils.log('p2_list', p2_list)


        

    def tennis(self, fit_thres, q, p, r, m):
        #Generate q random rulues
        #33221
        #Outlook(3), Temperature(3), Humidity(2), Wind(2), PlayTennis(1)
        rules = []
        for _ in range(q):
            rules.append(self.generate_tennis_rule())
        # print('-'*20)

        P = self.generate_hypotheses(rules)
        if len(P) < p:
            return -1
        # p = len(P)

        # if self.verbose:
        #     print('-'*20)
        #     for i, h in enumerate(H):
        #         utils.log(f'h{i} {len(h)}', h)
        
        # self.evaluate(H[0])
        fitness = []
        for h in P:
            nCorrect = self.correct(h)
            # utils.log(f'Hypothesis {h} correct on {nCorrect} examples')
            fitness.append(nCorrect**2)
        
        # while max(fitness) < fit_thres:
        nn = 0
        while nn < 1:

            nn += 1
            Ps = []
            fitness = []
            #Probabilistically select (1-r)p members of P 
            p = len(P) #n hypotheses in this population
            n = math.ceil((1-r)*p)
            utils.log(f'Keeping {n} hypotheses from {p}')
          
            
            
            #Compute fitness suma
            for h in P:
                    nCorrect = self.correct(h)
                    fitness.append(nCorrect**2)
            fitnessSum = sum(fitness)
            fitnessCopy = copy.deepcopy(fitness)

            if fitnessSum == 0:
                utils.log('[Bad start!] No good rules, restarting...')
                return -1 
            
            Ps, err = self.select(n, P, fitnessCopy, fitnessSum)
            # Ps, err = self.selectEager(n, P, fitnessCopy)
            if err:
                return -1
            utils.log(f'New population: {Ps}')

            n = math.ceil((r*p)/2)
            utils.log(f'Selecting {n} pairs for crossover from {p}')
            err = True
            fitnessCopy = copy.deepcopy(fitness)
            while err:
                parents, err = self.selectEager(n*2, P, fitness)
                if err:
                    utils.log(f'[ERR] Reselecting cross over pairs')
            utils.log(f'Pairs: {parents}')
            
            random.shuffle(parents)
            offsprings = self.crossover(parents[0], parents[1])
    

            


