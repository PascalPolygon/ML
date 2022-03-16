import random
from math import e
from utils import Utils
import copy

utils = Utils()
class Net():
    def __init__(self, n_neurons, lr=0.01, maxEpoch = 100, momentum = 0, verbose=True):
        self.n_neurons = n_neurons
        self.verbose = verbose
        self.eta = lr
        self.maxEpoch = maxEpoch
        self.alpha = momentum #Momentum hyper parametere

        self.w = [] #weights
        self.a = [] #activations (value at unit only for hidden and output)
        self.x = [] #Unit values (Includes input and biases)

        self.lossHistory = []

        for i in range(len(n_neurons)-1):
            self.w.append(self.initLayerWeights(n_neurons[i], n_neurons[i+1]))
        
        # self.weight_update = copy.copy(self.w)

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

    def loss(self, outputs, targets):
        E = 0
        for output, target in zip(outputs, targets):
            for o_k, t_k in zip(output, target):
                E += (t_k - o_k)**2
        return E/2
    
    def train(self, inputs, targets, validationSet=None, lossThresh=5):

        self.lossHistory = []

        for epoch in range(self.maxEpoch):
            
            w_update = [] #Weight update at current iter. Used for adding momentum 

            outputs = []
            # outputs = self.tune_weights(inputs, targets)
            for i, (input, target) in enumerate(zip(inputs, targets)):
                out = self.feedForward(input)
                outputs.append(out)
                # w_update.append(self.backPropagate(target))
                if epoch == 0:
                    # w_update = self.backPropagate(target, i, 0) #No delta_w(n-1) on first iteration
                    w_update.append(self.backPropagate(target)) #No delta_w(n-1) on first iteration
                else:
                    # w_update = self.backPropagate(target, i, prev_w_update)
                    w_update.append(self.backPropagate(target, prev_w_update[i])) #previous weight update of this sample
                    
            prev_w_update = copy.deepcopy(w_update)

            loss = self.loss(outputs, targets)
            self.lossHistory.append(loss)

            #Keep 2 copies of weights: training, and best performing weights
            #Once training weights reach significantly higher error over stored weights -> termninate
            if validationSet is not None:
                valInputs = validationSet[0]
                valTargets = validationSet[1]

                valOutputs = []
                for input in valInputs:
                    valOutput = self.feedForward(input)
                    valOutputs.append(valOutput)

                valLoss = self.loss(valOutputs, valTargets)
                if epoch == 0:
                    bestValLoss = valLoss
                    bestWeights = copy.copy(self.w)
                else:
                    if (valLoss - bestValLoss) > lossThresh: #valLoss is greater than bestLoss
                        #Return stored weights and terminate
                        self.w = copy.copy(bestWeights)
                        utils.log(f'** Terminating training, best weights found at epoch {epoch}', None)
                        break
                    elif valLoss < bestValLoss:
                        bestValLoss = valLoss
                        bestWeights = copy.copy(self.w)

            if self.verbose:
                utils.log('epoch', epoch)
                utils.log('loss', loss)
                print('-'*10)


    def feedForward(self, inps):
        self.x = []
        self.a = []
        inputs = copy.copy(inps)
        if len(inputs) != self.n_neurons[0]:
            raise ValueError(f'[ERROR] Input vector of size {len(inputs)} mismatch network input of size {self.n_neurons[0]}')
        layerActivations = []

        prevLayerActivations = inputs #Previous layer activations
        for layerWeights in self.w:
            layerActivations = []
            for i, unitInWeights in enumerate(layerWeights):
                unitOut = 0
                #Summation loop
                for input, w in zip(prevLayerActivations, unitInWeights[:-1]): 
                    unitOut += input*w
                unitOut += unitInWeights[-1] #bias
                layerActivations.append(self.sigmoid(unitOut))
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
    
    def backPropagate(self, target, prev_weight_update=[]):
        delta_out = []
        
        out = self.x[-1] #Last units are output
        for o, t in zip(out, target):
            delta_out.append(o*(1-o)*(t-o)) #Derivative of sigmoid

        net_out = delta_out
        #Find errors in hiddden units
        hiddenUnits = self.x[1:-1] #Exclude input and output layers
        
        n_layers = len(hiddenUnits) #Number of hidden layers
        deltas = []
        for layer in range(n_layers, 0, -1):
            units = hiddenUnits[layer-1]
            delta_layer = []
            for h, o_h in enumerate(units):
                sensitivity = 0
                # utils.log('delta_out', delta_out)
                for k, delta in enumerate(delta_out): #Should be prev/next layer not delta_out
                    sensitivity += self.w[layer][k][h]*delta
                delta_layer.append(o_h*(1-o_h)*sensitivity)
            deltas.append(delta_layer)
            delta_out = delta_layer[:1]

        deltas.reverse() # reverse because you calculated deltas (out -> in), but weights are updated (in->out)
        deltas.append(net_out)

        weight_update = copy.deepcopy(self.w)

        for j in range(len(self.w)): #Layer
            for k in range(len(self.w[j])): #Unit
                for i in range(len(self.w[j][k])): #Weight
                    # Calculate weight update
                    weight_update[j][k][i] = self.eta*deltas[j][k]*self.x[j][i]
                    #Update weights
                    if prev_weight_update:
                        self.w[j][k][i] += weight_update[j][k][i] + self.alpha*prev_weight_update[j][k][i] #Gradient descent w momentum
                    else:
                        self.w[j][k][i] += weight_update[j][k][i]
