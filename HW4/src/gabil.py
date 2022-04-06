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
    
    # def generate_tennis_rule(self):
    #     rule = []
    #     for _ in range(11):
    #         rule.append(1 if random.random() > 0.5 else 0)
    #     # if self.verbose:
    #     #     utils.log('Random rule', rule)
    #     return rule 
    
    # def generate_iris_rule(self):
    #     rule = []
    #     for _ in range(28*2+1):
    #         rule.append(1 if random.random() > 0.5 else 0)
    #     # if self.verbose:
    #     #     utils.log('Random rule', rule)
    #     return rule 
    
    def generate_rule(self, l):
        rule = []
        for _ in range(l):
            rule.append(1 if random.random() > 0.5 else 0)
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

    def test_tennis_rule(self, rule, inputs, targets):
        nCorrect = 0
        for input, target in zip(inputs, targets):
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

    def test_iris_rule(self, rule, inputs, targets):
        nCorrect = 0
        nAttrs = 4
        for input, target in zip(inputs, targets):
            index = 0
            num_index = 0
            nAttrMatch = 0
            for i in range(nAttrs):
                num = ''
                min_ = ''
                max_ = ''

                min_list_start = index
                min_list_end = index+7

                max_list_start = min_list_end
                max_list_end = max_list_start + 7

                index = max_list_end

                num_start = num_index
                num_end = num_start + 7
                num_index = num_end

                min_list = rule[min_list_start:min_list_end]
                max_list = rule[max_list_start:max_list_end]
                num_list = input[num_start:num_end]

                for i in range(len(min_list)):
                    min_ +=  str(min_list[i])

                for i in range(len(max_list)):
                    max_ += str(max_list[i])
                
                for i in range(len(num_list)):
                    num += str(num_list[i])

                # print(f'{min_} | {num} | {max_}')
                min_  = int(min_, 2)
                num  = int(num, 2)
                max_  = int(max_, 2)
                # print(f'{min_} | {num} | {max_}')
                if min_ < num and max_ > num:
                    nAttrMatch += 1
            pred = rule[-3:]

            if nAttrMatch == nAttrs:
                #Check that classifications match
                if pred == target:
                    nCorrect += 1

        return nCorrect

    def correct_tennis(self, h, inputs=None, targets=None):
        if inputs is None:
            inputs = copy.deepcopy(self.inputs)
            targets = copy.deepcopy(self.targets)
        #Extract individual rules from hypothesis
        rule = []
        nCorrect = 0 #n examples correctly classified by this hypothesis
        for bit in h:
            rule.append(bit)
            if len(rule) == 11:
                nCorrect += self.test_tennis_rule(rule, inputs, targets)
                rule = []
        return nCorrect

    def correct_iris(self, h, inputs=None, targets=None):

        if inputs is None:
            inputs = copy.deepcopy(self.inputs)
            targets = copy.deepcopy(self.targets)
        #Extract individual rules from hypothesis
        rule = []
        nCorrect = 0 #n examples correctly classified by this hypothesis
        for bit in h:
            rule.append(bit)
            if len(rule) == (28*2+3):
                nCorrect += self.test_iris_rule(rule, inputs, targets)
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
    
    # def rankSelect(self, n, P, fitnessCopy):


    def tournamentSelect(self, n, P, fitnessCopy, pr=0.7):
        nLoop = 0
        selected = []
        selected_ids = []
        # utils.log('Tournament selecting...')

        while len(selected) < n:
            if nLoop == 70:
                utils.log('[Bad start!] Likely due to not enough fit individuals, restarting...')
                return None, True
            
            fitnessSum = sum(fitnessCopy)

            #Randomly select individuals if there are no fit ones left
            if fitnessSum == 0:
                #Select a hypothesis at random
                random_selectable = []
                for i in range(len(fitnessCopy)):
                    if not i in selected_ids:
                        random_selectable.append(i)
                random_select = random.choice(random_selectable)
                # utils.log(f'Randomly selected h[{random_select}]')
                selected_ids.append(random_select)
                selected.append(P[random_select])
                if len(selected) == n:
                        break
            else:
                #Select 2 at random
                nn = len(P)
                i1 = random.randint(0, nn-1)
                i2 = random.randint(0, nn-1)
                # utils.log('Picking i1, i2')
                # while i1 in selectedIndices or i2 in selectedIndices:
                #     i1 = random.randint(0, n-1)
                #     i2 = random.randint(0, n-1)
                # print('Picking i1, i2')
                while fitnessCopy[i1] == 0 and fitnessCopy[i2] == 0:
                    i1 = random.randint(0, nn-1)
                    i2 = random.randint(0, nn-1)
                # print('i1, i2, picked!')
                # #Do not reuse already selected ones    
                # fitnessCopy[i1] = 0
                # fitnessCopy[i2] = 0
                h = [P[i1], P[i2]]
                # h1 = P[i1]
                # h2 = P[i2]
                #fitness
                # f = [(self.correct_iris(h[0]))**2, (self.correct_iris(h[1]))**2]
                f = [fitnessCopy[i1], fitnessCopy[i2]]
                iMax = f.index(max(f))
                if random.random() <= pr:
                    idx = iMax
                    # selectedIndices.append(idx)
                    selected.append(h[idx])
                else:
                    idx = int(1-iMax)
                    # selectedIndices.append(idx)
                    selected.append(h[idx])
                
                # utils.log('len selected', len(selected))

                #Set fitness of used hypothesis to low score so we don't reuse it
                if idx == 0:
                    fitnessCopy[i1] = 0
                else:
                    fitnessCopy[i2] = 0

                if len(selected) >= n:
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
                    # utils.log(f'Randomly selected h[{random_select}]')
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

    def calculate_d(self, p, h, l):
        nBoundaries = int(len(h)/l)
        # boundaries = [(i*l) if i > 0 else (i*l) for i in range(nBoundaries)]
        boundaries = [(i*l) for i in range(nBoundaries)]
        # utils.log('boundaries h', boundaries)
        steps = 0
        for i in range(p, -1, -1): #Step left throught the bit string until you reach the next boundary (to the left)
            if i in boundaries:
                return steps
            steps += 1


    def crossover(self, h1, h2, l=11):
        p1 = p2 = 0

        # utils.log('Getting the ps...')
        while not p1 < p2:
            p1 = random.randint(0, len(h1)-2)
            p2 = random.randint(p1, len(h1)-1)

        # utils.log('h1', h1)
        # utils.log('p1', p1)
        # utils.log('p2', p2)
        # utils.log('Calculating h1 ds...')
        d1 = self.calculate_d(p1, h1, l)
        d2 = self.calculate_d(p2, h1, l)
        # utils.log('d1', d1)
        # utils.log('d2', d2)
        p1_list = []
        p2_list = []
        # utils.log('Getting h2 ps...')
        for i in range(len(h2)):
            test_d1 = self.calculate_d(i, h2, l)
            test_d2 = self.calculate_d(i, h2, l)
            if test_d1 == d1:
                p1_list.append(i)
            if test_d2 == d2:
                p2_list.append(i)
        # utils.log('p1_list', p1_list)
        # utils.log('p2_list', p2_list)
        # utils.log('Random choice...')
        h2_p2 = h2_p1 = 0 
        nTrials = 0
        while not h2_p2 > h2_p1:
            if nTrials > 50:
                return -1
            h2_p1 = random.choice(p1_list)
            h2_p2 = random.choice(p2_list)
            nTrials += 1
        # utils.log('h2_p1', h2_p1)
        # utils.log('h2_p2', h2_p2)

        #Crossover points are points following points of intrest
        p2 += 1
        p1 += 1
        h2_p1 += 1
        h2_p2 += 1

        children = []

        # utils.log("Making child 1...[ please don't disturb ;) ]")
        child = copy.deepcopy(h2)
        child[h2_p1:h2_p2]=h1[p1:p2]
        children.append(child)

        # utils.log("Making child 2...[ please don't disturb ;) ]")
        child = copy.deepcopy(h1)
        child[p1:p2]=h2[h2_p1:h2_p2]
        children.append(child)
        return children
    
    def rankSelect(self, n, P, fitnessCopy):
        selected = []
        selected_ids = []
        # utils.log('Selecting...')
        # rankedP = copy.deepcopy(P)
        while len(selected) < n:

            fitnessSum = sum(fitnessCopy)

            if fitnessSum == 0:
                #Select a hypothesis at random
                random_selectable = []
                for i in range(len(fitnessCopy)):
                    if not i in selected_ids:
                        random_selectable.append(i)
                random_select = random.choice(random_selectable)
                # utils.log(f'Randomly selected h[{random_select}]')
                selected_ids.append(random_select)
                selected.append(P[random_select])
                if len(selected) == n:
                        break
            else:
                # fitnessCopy.sort()
                
                rankedP = [x for _,x in sorted(zip(fitnessCopy,P))]

                # for h in rankedP:
                #     utils.log(f'ranked hypo fitness', self.correct_iris(h)**2)
                # utils.log('sorted fitnessCopy', fitnessCopy)

                # rankedFitness = copy.deepcopy(fitnessCopy)
                # rankedFitness.sort()
                #We want desceding order
                # rankedFitness.reverse()
                rankedP.reverse()

                # utils.log('sorted fitness', rankedFitness)
                nn = len(rankedP)-1

                for i, h, in enumerate(rankedP):
                    selectProb = (nn-i)/nn
                    # utils.log(f'select prob at index {i}', selectProb)
                    if random.random() <= selectProb:
                        selected.append(h)
                        # utils.log(f'selected hypo at index {i} w fitness', (self.correct_iris(h)**2))
                        fitnessCopy[i] = 0 #do not reuse hypotheses
                        if len(selected)  == n:
                            break
                P = copy.deepcopy(rankedP)
        
        return selected, False


        

    def irisSelection(self, fit_thresh, q, p, r, m, max_gen, sel_strategy):
        rules = []
        for _ in range(q):
            rules.append(self.generate_rule((28*2)+3))
        utils.log('Generating population...')
        P = self.generate_hypotheses(rules)

        if p is not None:
            if len(P) < p:
                return -1
        
        fitness = []

        for h in P:
            nCorrect = self.correct_iris(h)
            fitness.append(nCorrect**2)
        fitnessSum = sum(fitness)
        utils.log(f'FITNESS {len(fitness)}', fitness)
        n_gen = 0

        utils.log('Starting evolution...')
        
        while n_gen < max_gen:
            if fit_thresh is not None:
                if max(fitness) >= fit_thresh:
                    utils.log('Max fitness reached!')
                    break
            Ps = []
            p = len(P) #n hypotheses in this population

            n = math.floor((1-r)*p)

            fitnessCopy = copy.deepcopy(fitness)

            if fitnessSum == 0:
                utils.log('[Bad start!] No good rules, restarting...')
                return -1 

            # Ps, err = self.selectEager(n, P, fitnessCopy)
            # utils.log('n to keep', n)
            err = False
            if sel_strategy == 'fitness_proportional':
                Ps, err = self.selectEager(n, P, fitnessCopy)
            elif sel_strategy == 'tournament':
                Ps, err = self.tournamentSelect(n, P, fitnessCopy, pr=0.8)
            elif sel_strategy == 'rank':
                Ps, err = self.rankSelect(n, P, fitnessCopy)
            # utils.log('P size after selection', len(Ps))

            if err:
                return -1
            
            n = math.ceil((r*p)/2)
            # utils.log('n babies', n*2)
            err = True
            # fitnessCopy = copy.deepcopy(fitness)
            # print('Selecting parents..')
            while err:
                if sel_strategy == 'fitness_proportional':
                    parents, err = self.selectEager(n*2, P, fitnessCopy)
                elif sel_strategy == 'tournament':
                    parents, err = self.tournamentSelect(n*2, P, fitnessCopy, pr=0.8)
                elif sel_strategy == 'rank':
                    parents, err = self.rankSelect(n*2, P, fitnessCopy)
                if err:
                    utils.log(f'[ERR] Reselecting cross over pairs')

            # print('Crossing over...')
            random.shuffle(parents)
            for i in range(0, len(parents)-1, 2):
                children = self.crossover(parents[i], parents[i+1], l=((28*2)+3))
                # utils.log('n produced children', len(children))
                if children == -1:
                    utils.log(f'[ERR] Got stuck in random choice')
                    return -1
                Ps += children
            # utils.log('P size after crossover', len(Ps))
            n = math.ceil(m*len(Ps)) #mutate
            for i in range(n):
                m_id = random.randint(0, len(Ps)-1)
                pos = random.randint(0, len(Ps[m_id])-1)
                Ps[m_id][pos]  = 1 -  Ps[m_id][pos]

            P = copy.deepcopy(Ps)
            # utils.log('New P size', len(P))
            fitness = []
            for h in P:
                nCorrect = self.correct_iris(h)
                fitness.append(nCorrect**2)
            fitnessSum = sum(fitness)
            utils.log(f'Generation', n_gen)
            utils.log(f'FITNESS {len(fitness)}', fitness)
            n_gen += 1
        return P

    def iris(self, fit_thresh, q, p, r, m, max_gen):
        rules = []
        for _ in range(q):
            rules.append(self.generate_rule((28*2)+3))
        utils.log('Generating population...')
        P = self.generate_hypotheses(rules)

        # utils.log('len(P)', len(P))
        if p is not None:
            if len(P) < p:
                return -1
        
        fitness = []

        for h in P:
            nCorrect = self.correct_iris(h)
            fitness.append(nCorrect**2)
        fitnessSum = sum(fitness)
        # utils.log(f'fitness {len(fitness)}', fitness)
        n_gen = 0

        utils.log('Starting evolution...')
        while max(fitness) < fit_thresh and n_gen < max_gen:
            Ps = []
            p = len(P) #n hypotheses in this population
            # utils.log(f'len(P)', p)
            n = math.floor((1-r)*p)
            # utils.log('n to keep', n)

            fitnessCopy = copy.deepcopy(fitness)

            if fitnessSum == 0:
                utils.log('[Bad start!] No good rules, restarting...')
                return -1 
            
            # print('Selecting next gen...')
            # Ps, err = self.select(n, P, fitnessCopy, fitnessSum)
            Ps, err = self.selectEager(n, P, fitnessCopy)

            if err:
                return -1

            # print('Selected')
            

            n = math.ceil((r*p)/2)
            # utils.log('n babies', n*2)
            err = True
            fitnessCopy = copy.deepcopy(fitness)
            # print('Selecting parents..')
            while err:
                parents, err = self.selectEager(n*2, P, fitness)
                if err:
                    utils.log(f'[ERR] Reselecting cross over pairs')

            # print('Crossing over...')
            random.shuffle(parents)
            for i in range(0, len(parents)-1, 2):
                children = self.crossover(parents[i], parents[i+1], l=((28*2)+3))
                if children == -1:
                    utils.log(f'[ERR] Got stuch in random choice')
                    return -1
                Ps += children
            n = math.ceil(m*len(Ps)) #mutate
            for i in range(n):
                m_id = random.randint(0, len(Ps)-1)
                pos = random.randint(0, len(Ps[m_id])-1)
                Ps[m_id][pos]  = 1 -  Ps[m_id][pos]

            P = copy.deepcopy(Ps)
            # utils.log('New P size', len(P))
            fitness = []
            for h in P:
                nCorrect = self.correct_iris(h)
                fitness.append(nCorrect**2)
            fitnessSum = sum(fitness)
            utils.log(f'Generation', n_gen)
            utils.log(f'FITNESS {len(fitness)}', fitness)
            n_gen += 1
        return P

    def tennis(self, fit_thres, q, p, r, m, max_gen):
        #Generate q random rulues
        #33221
        #Outlook(3), Temperature(3), Humidity(2), Wind(2), PlayTennis(1)
        rules = []
        for _ in range(q):
            rules.append(self.generate_rule(11))
        # print('-'*20)

        P = self.generate_hypotheses(rules)
        if p is not None:
            if len(P) < p:
                return -1
        # p = len(P)

        # if self.verbose:
        #     print('-'*20)
        #     for i, h in enumerate(H):
        #         utils.log(f'h{i} {len(h)}', h)
        
        # self.evaluate(H[0])
        fitness = []
        # for h in P:
        #     nCorrect = self.correct(h)
        #     # utils.log(f'Hypothesis {h} correct on {nCorrect} examples')
        #     fitness.append(nCorrect**2)
        for h in P:
            nCorrect = self.correct_tennis(h)
            fitness.append(nCorrect**2)
        fitnessSum = sum(fitness)
        # fitnessCopy = copy.deepcopy(fitness)
        n_gen = 0
        # while max(fitness) < fit_thres or n_gen < max_gen:
        # while max(fitness) < fit_thres:
        while max(fitness) < fit_thres and n_gen < max_gen:
            # utils.log('n_gen', n_gen)
        # nn = 0
        # while nn < 1:

            # nn += 1
            Ps = []
            # fitness = []
            #Probabilistically select (1-r)p members of P 
            p = len(P) #n hypotheses in this population
            # n = math.ceil((1-r)*p)
            n = math.floor((1-r)*p)
            # utils.log(f'Keeping {n} hypotheses from {p}')
            # utils.log('FITNESS', fitness)
            fitnessCopy = copy.deepcopy(fitness)

            
            #Compute fitness suma
            # for h in P:
            #         nCorrect = self.correct(h)
            #         fitness.append(nCorrect**2)
            # fitnessSum = sum(fitness)
            # fitnessCopy = copy.deepcopy(fitness)

            if fitnessSum == 0:
                utils.log('[Bad start!] No good rules, restarting...')
                return -1 
            
            Ps, err = self.select(n, P, fitnessCopy, fitnessSum)
            # Ps, err = self.selectEager(n, P, fitnessCopy)
            if err:
                return -1
            # utils.log(f'New population: {Ps}')

            n = math.ceil((r*p)/2)
            # utils.log(f'Selecting {n} pairs for crossover from {p}')
            err = True
            fitnessCopy = copy.deepcopy(fitness)
            while err:
                parents, err = self.selectEager(n*2, P, fitness)
                # utils.log('Outside select eager')
                if err:
                    utils.log(f'[ERR] Reselecting cross over pairs')
            # utils.log(f'Pairs: {parents}')
            # utils.log('Shuffling...')
            random.shuffle(parents)
            # utils.log('Crossing over...')
            for i in range(0, len(parents)-1, 2):
                children = self.crossover(parents[i], parents[i+1])
                if children == -1:
                    utils.log(f'[ERR] Got stuch in random choice')
                    return -1
                # utils.log('Children', children)
                Ps += children
            # utils.log('New Population', Ps)
            #mutate
            n = math.ceil(m*len(Ps))
            # utils.log(f'Mutate {n} individuals')
            # utils.log('Mutating..')
            for i in range(n):
                m_id = random.randint(0, len(Ps)-1)
                # utils.log(f'Mutating {m_id}', Ps[m_id])
                pos = random.randint(0, len(Ps[m_id])-1)
                # utils.log('bit', pos)
                Ps[m_id][pos]  = 1 -  Ps[m_id][pos]
                # utils.log('Mutated   ', Ps[m_id])

            P = copy.deepcopy(Ps)

            #Eval performance
            fitness = []
            for h in P:
                nCorrect = self.correct_tennis(h)
                fitness.append(nCorrect**2)
            fitnessSum = sum(fitness)
            utils.log('FITNESS', fitness)
            n_gen += 1
            # fitnessCopy = copy.deepcopy(fitness)
        return P
        # utils.log('FITNESS', fitness)
    

            


