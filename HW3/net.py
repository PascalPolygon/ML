import enum
import random
from math import e


class Net():
    def __init__(self, n_neurons):
        self.n_neurons = n_neurons
        self.w = [] #weights
        self.a = [] #activations (value at unit only for hidden and output)
        self.x = [] #Unit values (Includes input and biases)
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
        
        #Create unit value list
        inputs.append(1) #Bias unit
        self.x.append(inputs)
        for i, a in enumerate(self.a):
            if (i < len(self.a)-1): #Not Output units
                a.append(1) #bias unit
            self.x.append(a)
        
        return self.a[-1] #Only return last layer (outut layer) activation
    
    def backPropagate(self, target, eta = 0.01):
        delta_out = []
        
        out = self.x[-1] #Last units are output
        for o, t in zip(out, target):
            delta_out.append(o*(1-o)*(t-o)) #Derivative of sigmoid

        net_out = delta_out
        #Find errors in hiddden units
        hiddenUnits = self.x[1:-1] #Exclude input and output layers
        print(hiddenUnits)
        delta_hidden = []
        
        n_layers = len(hiddenUnits) #Number of hidden layers
        deltas = []
        for layer in range(n_layers, 0, -1):
            # print(layer)
            # print(f'Delta out : {delta_out}')
            units = hiddenUnits[layer-1]
            delta_layer = []
            for h, o_h in enumerate(units):
                sensitivity = 0
                for k, delta in enumerate(delta_out): #Should be prev/next layer not delta_out
                    # print(f'k = {k}')
                    # print(f'h = {k}')
                    # print(self.w[layer])
                    sensitivity += self.w[layer][k][h]*delta
                delta_layer.append(o_h*(1-o_h)*sensitivity)
            # print(delta_layer)
            deltas.append(delta_layer)
            delta_out = delta_layer[:1]

        deltas.reverse() # reverse because you calculated deltas (out -> in), but weights are updated (in->out)
        # deltas.append(delta_hidden)
        deltas.append(net_out)
        # print(f'deltas = {deltas}')

        #Update weights
        for j in range(len(self.w)): #Layer
            for k in range(len(self.w[j])): #Unit
                for i in range(len(self.w[j][k])): #Weight
                    # self.x[j][i]
                    # print(f'j = {j}')
                    # print(f'k = {k}')
                    # deltas[j][k]
                    self.w[j][k][i] += eta*deltas[j][k]*self.x[j][i]

    # def backPropagate_(self, out, target, eta=0.01):
    #     TAG = 'BACK_PROP'
    #     #For each network output unit calculate its error term
    #     print('Back Propagate')
    #     deltas = []
    #     delta_out = []
    #     for o, t in zip(out, target):
    #         delta_out.append(o*(1-o)*(t-o)) #Derivative of sigmoid

    #     weights = self.w[-1]
    #     activations = self.a[-2]
    #     print(f'{TAG} delta out - : {delta_out}')
    #     print(f'{TAG} weights - : {weights}')
    #     print(f'{TAG} activations - : {self.a}')
    #     delta_hidden = []
    #     for h, o_h in enumerate(activations):
    #         #Summation loop
    #         sensitivity = 0
    #         for k, delta in enumerate(delta_out):
    #             sensitivity += weights[k][h]*delta
    #         delta_hidden.append(o_h*(1-o_h)*sensitivity)
        
        
    #     #Calculate error of bias unit (for hidden layer)
    #     sensitivity = 0
    #     for k, delta in enumerate(delta_out):
    #         sensitivity += weights[k][-1]*delta #Weight associated with bias unit
    #     delta_hidden.append(0.1966119332414823*sensitivity)
    #     #Calculate error of bias unit (for inut layer)
    #     sensitivity = 0
    #     for k, delta in enumerate(delta_hidden):
    #         sensitivity += weights[k][-1]*delta #Weight associated with bias unit
    #     #Outut of bias unit is always 1
    #     #sigmoid(1) =  0.7310585786300048792512
    #     # sigmoid(1)*(1 - sigmoid(1)) = 0.1966119332414823
        

    #     deltas.append(delta_hidden)
    #     deltas.append(delta_out)
    #     print(f'{TAG} deltas - : {deltas}')
        
    #     #Update weights
    #     for j in range(len(self.w)):
    #         for k in range(len(self.w[j])):
    #             for i in range(len(self.w[j][k])):
    #                 if i == len(self.w[j][k])-1: #This is the bias unit
    #                     self.w[j][k][i] =  self.w[j][k][i] + eta*deltas[j][i]
    #                 else:
    #                     print(f'i = {i}, j = {j}, k={k}')
    #                     print(self.a[j][i])
    #                     # self.w[j][k][i] =  self.w[j][k][i] + eta*deltas[j][i]*self.a[j][i]
        

        #Layer 1, unit 1, weight 1    #Delta of layer 1, unit 1, activation of layer 1, unit 1
        # self.w[0][0][0] = self.w[0][0][0] + eta*deltas[0][0]*self.a[0][0] #1st layer, 1st unit, 1st weight
        # self.w[0][0][1] = self.w[0][0][1] + eta*deltas[0][1]*self.a[0][1] #1st layer, 1st unit, 2nd weight
        # self.w[0][0][2] = self.w[0][0][2] + eta*deltas[0][2]*self.a[0][2] #1st layer, 1st unit, 3rd weight

        # self.w[0][-1][0] = self.w[0][-1][0] + eta*deltas[0][0]*1 #1st layer, bias unit, 1st weight
        # self.w[0][-1][1] = self.w[0][-1][1] + eta*deltas[0][1]*1 #1st layer, bias unit, 2nd weight
        # self.w[0][-1][2] = self.w[0][-1][2] + eta*deltas[0][2]*1 #1st layer, bias unit, 3rd weight

        # self.w[1][-1][0] = self.w[1][-1][0] + eta*deltas[1][0]*1 #2nd layer, bias unit, 1st weight
        # self.w[1][-1][1] = self.w[1][-1][1] + eta*deltas[1][1]*1 #2nd layer, bias unit, 2nd weight
