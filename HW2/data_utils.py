class DataUtils():
    def __init__(self, verbose=False):
        # self.data = []
        self.verbose = verbose

    def get_labels(self, examples):
        labels = []
        for example in examples:
            labels.append(example[-1])
        return labels

    def find_best_attr(self, examples, attributes):
        if self.verbose:
            print(examples)

    # def is_pure(self, data):
    #     self.
