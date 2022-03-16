```
optional arguments:
  -h, --help            show this help message and exit
  --max_iter MAX_ITER   max training iterations
  --lr LR               learning rate
  --momentum MOMENTUM   momentum hyperparameter
  --hidden_units HIDDEN_UNITS
                        number of hidden units
  --validation VALIDATION
                        percentage of data to keep for validation
  --hidden_arch HIDDEN_ARCH
                        customer hidden layers architecture. Format:
                        #units-#units-#units (e.g. 1-3-2)
  --verbose VERBOSE     verbose
  --loss_thresh LOSS_THRESH
                        Maximum difference between loss of bestweights vs
                        training weights on validation data
```

## Example run commands:
```
  python3 testIdentity.py --max_iter 10 --lr 5 

  python3 testTennis.py --max_iter 10 --lr 5 --hidden_units 4

  python3 testIrisNoisy.py --validation 0.3 --momentum 0.1
  
  python3 testIris.py --validation 0.3 --momentum 0.1 --hidden_arch 3-4
```

**Notes on hidden_arch:**
  In this implementation, it is possiblie to construct networks with multiple hidden layers not just 1. By default a network with 1 hidden layer is constructed with 3 hidden units. The number of hidden units can be set by the user with the ```--hidden_units``` option. To construct networks with multiple hidden layers, use ```--hidden_arch```. For example the option ```--hidden_arch 3-4-3``` will have 3 hidden layers with 3, 4 and 3 hidden units respectively. 

## Running testIdentity
It was found that testIdentity achieves the best performance when using a high learning rate, lr=5 was used while testing.