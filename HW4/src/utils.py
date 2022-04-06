import inspect
import argparse
import random
class Utils:
    def __init__(self):
        self.data = []
    
    def toFloat(self, data):
        for i, example in enumerate(data):
            data[i] = list(map(float, example))
        return data
    
    def toBin(self, data, scale=1):
        binData = []
        for i, example in enumerate(data):
            binStr = ''
            for j in range(len(example)):
                integer =  int(float(example[j])*scale) # convert to scaled int instead (can be rep as 7bit num w no restriction on crossover)
                binStr += '{0:07b}'.format(integer)
                # exampleStr += binStr
            binList = []
            for k in range(len(binStr)):
                binList.append(int(binStr[k])) 
            binData.append(binList)
        return binData
        
    def log(self, name, data=None):
        TAG = inspect.stack()[1][3] #Name of function who called
        print(f'{TAG} {name} - {data}')

    def load_examples(self, file):
        trainingExamples = []
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                example = line.split(' ')
                trainingExamples.append(example)
        return trainingExamples
    
    def make_readable(self, rule):

        outlook_rule = rule[:3]
        outlook_readable_rule = 'Outlook = '
        if sum(outlook_rule) == 3:
            outlook_readable_rule += 'Any '
        elif sum(outlook_rule) == 0:
            outlook_readable_rule += 'None '
        else:
            if outlook_rule[0] == 1:
                outlook_readable_rule += 'Sunny'
            if outlook_rule[1] == 1:
                if  outlook_readable_rule == 'Outlook = ':
                    outlook_readable_rule += ' Overcast'
                else:
                    outlook_readable_rule += ' V Overcast'
            if outlook_rule[2] == 1:
                if  outlook_readable_rule == 'Outlook = ':
                    outlook_readable_rule += ' Rain'
                else:
                    outlook_readable_rule += ' V Rain'

        temp_rule = rule[3:6]
        temp_readable_rule = 'Temp = '
        if sum(temp_rule) == 3:
            temp_readable_rule += 'Any '
        elif sum(temp_rule) == 0:
            temp_readable_rule += 'None '
        else:
            if temp_rule[0] == 1:
                temp_readable_rule += 'Hot'
            if temp_rule[1] == 1:
                if  temp_readable_rule == 'Temp = ':
                    temp_readable_rule += ' Mild'
                else:
                    temp_readable_rule += ' V Mild'
            if temp_rule[2] == 1:
                if  temp_readable_rule == 'Temp = ':
                    temp_readable_rule += ' Cool'
                else:
                    temp_readable_rule += ' V Cool'


        hum_rule = rule[6:8]
        hum_readable_rule = 'Hum = '
        if sum(hum_rule) == 2:
            hum_readable_rule += 'Any '
        elif sum(hum_rule) == 0:
            hum_readable_rule += 'None '
        else:
            if hum_rule[0] == 1:
                hum_readable_rule += 'High'
            if hum_rule[1] == 1:
                if  hum_readable_rule == 'Hum = ':
                    hum_readable_rule += ' Normal'
                else:
                    hum_readable_rule += 'V Normal'
        

        wind_rule = rule[8:10]
        wind_readable_rule = 'Wind = '
        if sum(wind_rule) == 2:
            wind_readable_rule += 'Any '
        elif sum(wind_rule) == 0:
            wind_readable_rule += 'None '
        else:
            if wind_rule[0] == 1:
                wind_readable_rule += 'Weak'
            if wind_rule[1] == 1:
                if  wind_readable_rule == 'Wind = ':
                    wind_readable_rule += ' Strong'
                else:
                    wind_readable_rule += 'V Strong'

        pred = rule[10]
        pred_readable_rule = 'PlayTennis = ' 
        pred_readable_rule += 'Yes' if pred == 1 else 'No'
        readable_rule = '('+ outlook_readable_rule+') ^ ('+ temp_readable_rule + ') ^ (' + hum_readable_rule + ') ^ (' + wind_readable_rule + ') ^ (' + pred_readable_rule + ')' 
        return readable_rule

    def make_iris_readable(self, rule):
        #make a radom rule for testing
        # rule = []
        # for i in range((28*2)+3):
        #     rule.append(random.randint(0,1))
        # print(rule)
        
        nAttrs = 4
        attrs = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width']
        index = 0
        ruleStr = ''
        for j in range(nAttrs):
            min_ = ''
            max_ = ''

            min_list_start = index
            min_list_end = index+7

            max_list_start = min_list_end
            max_list_end = max_list_start + 7

            index = max_list_end

            min_list = rule[min_list_start:min_list_end]
            max_list = rule[max_list_start:max_list_end]

            for i in range(len(min_list)):
                # print(min_list[i])
                min_ +=  str(min_list[i])

            for i in range(len(max_list)):
                max_ += str(max_list[i])

            # print(min_)
            min_  = int(min_, 2)
            max_  = int(max_, 2)

            if j != 0:
                ruleStr += f'^({float(min_)/10} < {attrs[j]} < {float(max_)/10})'
            else:
                ruleStr += f'({float(min_)/10} < {attrs[j]} < {float(max_)/10})'
        
        pred = rule[-3:]
        if pred == [1,0,0]:
            flower = 'Iris-setosa'
        elif pred == [0,1,0]:
            flower = 'Iris-versicolor'
        elif pred == [0,0,1]:
            flower = 'Iris-virginica'
        else:
            flower = 'unknown'
        ruleStr += f'^(Flower = {flower})'
        return ruleStr
    
    def display_tennis_rules(self, P):
        readable_rules = []
        # rule = [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0]
        for h in P:
            rule = []
            # readable_rule = []
            hypo_rules = []
            for bit in h:
                rule.append(bit)
                if len(rule) == 11:
                    aRule = self.make_readable(rule)
                    # print(aRule)
                    hypo_rules.append(aRule)
                    rule = []
            readable_rules.append(hypo_rules)
            hypo_rules = []
        return readable_rules
                
    def display_iris_rule(self, P):
        # print(self.make_iris_readable([]))
        readable_rules = []
        for h in P:
            rule = []
            # readable_rule = []
            hypo_rules = []
            for bit in h:
                rule.append(bit)
                if len(rule) == (28*2)+3:
                    aRule = self.make_iris_readable(rule)
                    # print(aRule)
                    hypo_rules.append(aRule)
                    rule = []
            readable_rules.append(hypo_rules)
            hypo_rules = []
        return readable_rules

    def arg_parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--q", help="Number of individual rules", default=500)
        parser.add_argument("--r", help="Replacement rate", default=0.6)
        parser.add_argument("--m", help="Mutation rate", default=0.001)
        parser.add_argument("--fitness_thresh", help="Fitness threshold stopping criterio", default=None)
        parser.add_argument("--max_gen", help="Number of generation  stopping criterion", default=50)
        parser.add_argument("--sel_strategy", help="Selection strategy", default='fitness-proportional')
        # parser.add_argument("--validation", help="percentage of data to keep for validation", default=0)
        # parser.add_argument("--hidden_arch", help="customer hidden layers architecture. Format: #units-#units-#units (e.g. 1-3-2)", default='3')
        parser.add_argument("--verbose", help="verbose", default=False)
        # parser.add_argument("--loss_thresh", help="Maximum difference between loss of bestweights vs training weights on validation data", default=0.1)
        
        opt = parser.parse_args()
        if opt.verbose == 'False': 
            opt.verbose = False
        elif opt.verbose =='True':
            opt.verbose = True

        if opt.fitness_thresh == 'None':
            opt.fitness_thresh == None
        return opt