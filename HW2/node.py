class Node:
    def __init__(self, attr, attrVals):
        self.attr = attr
        self.values = {}
        if attrVals is not None:
            for v in attrVals:
                self.values[v] = None
