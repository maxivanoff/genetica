from mpi4py import MPI

from common import Output
from multi import Environment
from fitness.test import localglobal
from fitness.test import quadratic

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
graphics = True # plots matplotlib graphs

problem_name = 'quadratic_mod'

# Objectives
objectives = ['objective1', 'objective2']

# GA settings
size=18 #population size
num_cycles=1 # number of GA cycles
cross_rate = 1.0
mutation_rate = 0.0

# Convergence criteria
max_gen=500 # Maximum number of generations

# Names and Ranges of Variables
var_ranges = {
        'X1': [-10, 10],\
        }

function = quadratic.Fitness(problem_name, objectives, comm=comm, size=size)

if rank==0:
    output = Output.Output(problem_name, objectives, var_ranges, max_gen, size, cross_rate, mutation_rate, graphics) 
    env = Environment.VEGAEnvironment(objectives, var_ranges, size, max_gen, cross_rate, mutation_rate, num_cycles,function, output)
    env.run()
else:
    function.slaves_work()
