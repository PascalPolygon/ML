import random
from math import e


class Net():
    def __init__(self, n_neurons):
        self.n_neurons = n_neurons
        self.w = [] #weights
        self.a = [] #activations (value at unit)
        for i in range(len(n_neurons)-1):
            self.w.append(self.initLayerWeights(n_neurons[i], n_neurons[i+1]))

    def initLayerWeights(self, n_in_units, n_out_units):
        layerWeights = []
        for j in range(n_out_units):
            weights = []
            for i in range(n_in_units+1):
                weights.append(random.uniform(-0.5, 0.5))
            layerWeights.append(weights)
        return layerWeights
    
    def sigmoid(self, x):
        return (1/(1+e**-x))

    def feedForward(self, inputs):
        #Activation for a single hidden unit
        if len(inputs) != self.n_neurons[0]:
            raise ValueError(f'[ERROR] Input vector of size {len(inputs)} mismatch network input of size {self.n_neurons[0]}')
        layerActivations = []
        # for layerWeights in self.w[0]:
        # layerWeights = self.w[0] #Only first layer
        prevLayerActivations = inputs #Previous layer activations
        for layerWeights in self.w:
            layerActivations = []
            for i, unitInWeights in enumerate(layerWeights):
        # unitInWeights = self.w[0][0] #Only for the first unit of teh first hidden layer
                unitOut = 0
                #Summation loop
                for input, w in zip(prevLayerActivations, unitInWeights[:-1]): 
                    unitOut += input*w
                unitOut += unitInWeights[-1] #bias
                # print(unitOut)
                layerActivations.append(self.sigmoid(unitOut))
            # if (i+1) <= len(self.w)  
            # layerActivations.append(layerWeights[i+1][-1]) #Bias: should be biased weight of the next layer
            self.a.append(layerActivations)
            prevLayerActivations = layerActivations
        return self.a[-1] #Only return last layer (outut layer) activation
    
    def backPropagate(self, out, target, eta=0.01):
        TAG = 'BACK_PROP'
        #For each network output unit calculate its error term
        print('Back Propagate')
        deltas = []
        delta_out = []
        for o, t in zip(out, target):
            delta_out.append(o*(1-o)*(t-o)) #Derivative of sigmoid

        weights = self.w[-1]
        activations = self.a[-2]
        print(f'{TAG} delta out - : {delta_out}')
        print(f'{TAG} weights - : {weights}')
        print(f'{TAG} activations - : {activations}')
        delta_hidden = []
        for h, o_h in enumerate(activations):
            #Summation loop
            sensitivity = 0
            for k, delta in enumerate(delta_out):
                sensitivity += weights[k][h]*delta
            delta_hidden.append(o_h*(1-o_h)*sensitivity)
        print(f'{TAG} delta hidden - : {delta_hidden}')

        deltas.append(delta_hidden)
        deltas.append(delta_out)
        print(f'{TAG} deltas - : {deltas}')

        #Layer 1, unit 1, weight 1    #Delta of layer 1, unit 1, activation of layer 1, unit 1
        self.w[0][0][0] = self.w[0][0][0] + eta*deltas[0][0]*self.a[0][0]
        # for layerWeights in self.w:
        #     for unitWeights in layerWeights:
        #         for w in unitWeights:
        #             w = w + eta*deltas[layer][hidden_unit]


    
    #Weight matrix (for input -> hidden) will have (n_in + 1) rows and n_h columns
    #Weight matrix (for hidden -> output) will have (n_h + 1) rows and n_out columns
    #Init weight matrix

