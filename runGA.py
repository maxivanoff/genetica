from mpi4py import MPI

from Output import Output
from genetica import Environment, Population, Individual
from fitness import Fitness

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
graphics = True # plots matplotlib graphs

problem_name = 'canyon'

# Objectives
objectives = ['objective1', 'objective2']

# GA settings
size=27 #population size
num_cycles=1 # number of GA cycles
cross_rate = 0.7
mutation_rate = 0.03

# Convergence criteria
max_gen=200 # Maximum number of generations


# Names and Ranges of Variables
var_ranges = {
        'X1': [-1,1],\
        'X2': [-1,1],\
        }


fitness = Fitness(problem_name, objectives, comm=comm, size=size)

if rank==0:
    output = Output(problem_name, objectives, var_ranges, max_gen, size, cross_rate, mutation_rate, graphics) 
    env = Environment.Environment(objectives, var_ranges, size, max_gen, cross_rate, mutation_rate, num_cycles,  Individual.RealCoded, Population.Population, fitness, output)
    env.run()
else:
    fitness.slaves_work()
