```
optional arguments:
usage: [-h] [--q Q] [--r R] [--m M]
       [--fitness_thresh FITNESS_THRESH] [--max_gen MAX_GEN]
       [--sel_strategy SEL_STRATEGY] [--verbose VERBOSE]
```

**Notes on --q option**
 In this implementation, the population size p is automatically obtained for the ```--q``` argument which refers to total number of individual rules. The number of hypotheses is ```p``` is a consequence of randomly assigning ```q``` rules to various hypoetheses. See ```generate_hypotheses``` in ```gabil.py``` for more detail. 

**Notes on continous values**
 In this implementation, iris continous values are represented as a 7bit interger (in binary), instead of using IEEE 754 32 bit representation. This is done by first scaling the values by a factor of 10 and then converting to integer. Doing this allows unconstrained crossover as we don't have to be careful to avoid the sign and exponent bits during crossover.


**Note on running the program**
The Program will automatically restart if the initial hypotheses of 0 accuracy on the training data. This restart may happen several time. Please be patient.
## Example run commands:
```
  python3 testTennis.py --fitness-thresh 100 --q 1000 #--fitness-thres is a required argument for testTennis.py

  python3 testIris.py --fitness-thresh 100 --q 1000 --sel_stragegy rank # --fitness-thres is a required argument for testIris.py

  python3 testIrisSelection.py --max_gen 100 --q 1000

  python3 testIrisReplacement.py --max_gen 2