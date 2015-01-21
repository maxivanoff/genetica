genetica 
====
Python library for minimization of a function using genetic algorithms in parallel.
---

Requirements:
* mpi4py - MPI parallelization
* matplotlib - graphical representation of results

Content:
* fitness.py - defines function to minimize, as an example function f(x,y) = 0.1x^2 + |y| is minimized
* Environment.py - sets the general structure of the algorithm
* Population.py - defines properties of a populations
* Individual.py - defines properties of an individual chromosome
* IO.py - basic output
* ioo.py - output with graphical representation
* runGA.py - launches the algorithm

This work was supported by the National Science Foundation (NSF) CAREER award CHE–1255641 and the Bournique Memorial Fellowship by Marquette University.

