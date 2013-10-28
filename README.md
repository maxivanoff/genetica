genetica 
========
Python library for minimization of a function using genetic algorithms in parallel.
--------

Author: Maxim Ivanov

Email: maxim.ivanov@marquette.edu

Requirements:

* mpi4py - MPI parallelization
* matplotlib - graphical representation of results

Content:

Environment.py - sets the general structure of the algorithm
Population.py - defines properties of a populations
Individual.py - defines properties of an individual chromosome
ioo.py - outputs results of optimization
runGA.py - launches the algorithm
fitness.py - defines function to minimize, as an example function f(x,y) = 0.1x^2 + |y| is minimized
