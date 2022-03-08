import inspect

class Utils:
    def __init__(self):
        self.data = []
    
    def toFloat(self, data):

        for i, example in enumerate(data):
            data[i] = list(map(float, example))
        return data
        
    def log(self, name, data):
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