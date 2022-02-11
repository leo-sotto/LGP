## About

This is a Linear Genetic Programming (LGP) implementation in Python and C++.

## Requirements

* Python 3 with Numpy.
* Swig, to make the interface with the evaluation function, which is in C++. With Anaconda, it can be installed via:

```
$ conda install -c anaconda swig
```

## How to Use

First, one needs to compile the C++ modules with Swig. For that, you need to replace the following in _compile\_swig.sh_ in the _code_ directory by the location 
in your machine.

```
-I/home/leo/anaconda3/include/python3.7m
```

After that, you need to run the script:

```
$ ./compile_swig.sh
```

The parameters that can be configured are explained in _parameters.py_, and _run\_single.py_ shows how to run the LGP algorithm. You can either set the parameters
in the _parameters.py_ file, instantiate a `Parameters` object, and pass it as argument when instantiating an `LGP` object, or change each parameter dinamically 
after instatiating the `Parameters` object. An example of this last option is shown in _run_parallel.py_, that runs different algorithm configurations on different
problems in parallel.

This repository includes some example problems in the directory _datasets_, but one can add more problems as long as the CSV files follow the same structure. It's 
also possible to add more non-terminal functions or fitness measures by changing the parameters class and the fitness evaluation code.

## Log Files

Each run generates some log files, that are stored in the location defined in your `Parameters` object. These files are:

* **bestEffSizes:** Effective size of the best program found at the last generation.
* **bestSizes:** Absolute size of the best program found at the last generation.
* **best_test_[MEASURE]:** Fitness of the best program found at the last generation, in the testing set. [MEASURE] refers to the measures defined in the 
`Parameters` object.
* **best_train_[MEASURE]:** Fitness of the best program found at the last generation, in the training set.
* **evaluations:** Fitness evaluations needed to find the optimal solution. -1 if the solution was not found.
* **instEvaluations:** Number of effective instruction evaluations needed to find the optimal solution. -1 if the solution was not found.
* **meanEffSizes:** Mean effective size of individuals in the population at the last generation.
* **meanSizes:** Mean absolute size of individuals in the population at the last generation.
* **mean_test_[MEASURE]:** Mean fitness of individuals in the population at the last generation, in the testing set.
* **mean_train_[MEASURE]:** Mean fitness of individuals in the population at the last generation, in the training set.
* **solutions:** Best program found, shown as a sequence of instructions.

If more runs are performed using a same log directory, each row in the CSV files correspond to a run. It is also possible to remove, change, or add log files by 
editing the code in _LGP.py_. For example, one may want to have the fitness values for all generations instead of only for the last one.

## Citation

This LGP implementation is from the following publication:

```
@article{SottoGraphGP2021,
  author    = {L{\'{e}}o Fran{\c{c}}oso Dal Piccol Sotto and Paul Kaufmann and Timothy Atkinson and Roman Kalkreuth and M{\'{a}}rcio Porto Basgalupp},
  title     = {Graph representations in genetic programming},
  journal   = {Genetic Programming and Evolvable Machines},
  volume    = {22},
  number    = {4},
  pages     = {607--636},
  year      = {2021},
  url       = {https://doi.org/10.1007/s10710-021-09413-9},
  doi       = {10.1007/s10710-021-09413-9}
}
```
