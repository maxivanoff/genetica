from mpi4py import MPI

import ioo
from genetica import Environment, Population, Individual
from fitness import Fitness

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

problem_name = 'canyon'

# Objectives
objectives = ['objective1', 'objective2']

# GA settings
size=21 #population size
num_cycles=1000 # number of GA cycles
cross_rate = 0.7
mutation_rate = 0.03

# Convergence criteria
max_gen=200 # Maximum number of generations
threshold = 0.0001
conv_gen = 10


# Names and Ranges of Variables
var_ranges = {
        'Y': [-1,1],\
        'X': [-1,1],\
        }


fitness = Fitness(problem_name, comm=comm, size=size)

if rank==0:
    output = ioo.Output(problem_name_tmp, var_ranges) 
    env = Environment.Environment(objectives, var_ranges, size, max_gen, threshold, conv_gen, cross_rate, mutation_rate, num_cycles,  Individual.RealCoded, Population.Population, fitness, output)
    env.run()
else:
    fitness.slaves_work()
