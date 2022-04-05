import inspect
import argparse

class Utils:
    def __init__(self):
        self.data = []
    
    def toFloat(self, data):
        for i, example in enumerate(data):
            data[i] = list(map(float, example))
        return data
        
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
        else:
            if outlook_rule[0] == 1:
                outlook_readable_rule += 'Sunny'
            if outlook_rule[1] == 1:
                if  outlook_readable_rule == 'Outlook = ':
                    outlook_readable_rule += ' Overcast'
                else:
                    outlook_readable_rule += 'V Overcast'
            if outlook_rule[2] == 1:
                if  outlook_readable_rule == 'Outlook = ':
                    outlook_readable_rule += ' Rain'
                else:
                    outlook_readable_rule += 'V Rain'

        temp_rule = rule[3:6]
        temp_readable_rule = 'Temp = '
        if sum(temp_rule) == 3:
            temp_readable_rule += 'Any '
        else:
            if temp_rule[0] == 1:
                temp_readable_rule += 'Hot'
            if temp_rule[1] == 1:
                if  temp_readable_rule == 'Temp = ':
                    temp_readable_rule += ' Mild'
                else:
                    temp_readable_rule += 'V Mild'
            if temp_rule[2] == 1:
                if  temp_readable_rule == 'Temp = ':
                    temp_readable_rule += ' Cool'
                else:
                    temp_readable_rule += 'V Cool'


        hum_rule = rule[6:8]
        hum_readable_rule = 'Hum = '
        if sum(hum_rule) == 2:
            hum_readable_rule += 'Any '
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

    def display_rules(self, P):
        readable_rules = []
        rule = [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0]
        print(self.make_readable(rule))
        # for h in P:
        #     rule = []
        #     readable_rule = []
        #     for bit in h:
        #         rule.append(bit)
        #         if len(rule) == 11:
        #             readable_rule.append(self.make_readable(rule))
        #     readable_rules.append(readable_rule)
                    # nCorrect += self.test_rule(rule)
                    # rule = []
    
    def arg_parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--p", help="Population size", default=10)
        parser.add_argument("--r", help="Replacement rate", default=0.6)
        parser.add_argument("--m", help="Mutation rate", default=0.001)
        parser.add_argument("--fitness_thresh", help="Fitness threshold stopping criterio", default=0.9)
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

        return opt