from net import Net
import sys
from utils import Utils

utils = Utils()

# n_neur = [2, 3, 1]
# net = Net([8, 3, 8]) #2 units in input, 3 in hiddel and 1 in output layer


# print(len(net.w))
# for w in net.w:
#     print(w)
#     print('------')
# print(f'Initial weights : {net.w}') 
input = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
target = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# print(f'Input: {input}')
try:
    net = Net([8, 3, 8], lr=0.01, maxEpoch=50) 
    # for i in range(50):
    for i in range(10):
        out = net.feedForward(input)
        net.backPropagate(target)
    # utils.log('net x (After back prop)', len(net.x))

    # # print(input)
    # out = net.feedForward(input)
    # # utils.log('net x (2)', len(net.x))
    # # utils.log('input', input)
    # net.backPropagate(target)

    # print(f'Updated weights: {net.w}')
except ValueError as err:
    print(err)
    sys.exit()

    


# print(net.w)
