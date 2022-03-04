from net import Net
import sys

# n_neur = [2, 3, 1]
net = Net([2, 4, 2]) #2 units in input, 3 in hiddel and 1 in output layer


print(len(net.w))
# for w in net.w:
#     print(w)
#     print('------')
print(net.w[0]) 
input = [2.4, 1.3]
target = [5.8, 0.9]
print(f'Input: {input}')
try:
    out = net.feedForward(input)
    print(f'Output = {out}')
    print(f'Net activations: {net.a}')
    net.backPropagate(out, target)
except ValueError as err:
    print(err)
    sys.exit()

    


# print(net.w)
