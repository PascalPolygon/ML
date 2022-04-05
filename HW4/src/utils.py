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