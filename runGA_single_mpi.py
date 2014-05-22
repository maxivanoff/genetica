from mpi4py import MPI

from common import Output
from single import Environment
from fitness.test import funs
from fitness import FitnessFunction

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
graphics = True # plots matplotlib graphs

job_name = 'quadratic'

settingsGA = {'size': 9,\
                'crossover rate': 0.8,\
                'mutation rate': 0.03,\
                'maximum generations': 50,\
                'number GA cycles': 100}
# Objectives, all will be plotted at the end, but the first one will be optimized
objectives = ['objective2', 'objective1']

# Names and Ranges of Variables
var_ranges = {
        'X1': [-10, 10],\
        }

function = FitnessFunction.Parallel(objectives, funs.quadratic, comm=comm, size=settingsGA['size'])

if rank==0:
    output = Output.Output(job_name, objectives, var_ranges, settingsGA, graphics) 
    env = Environment.SingleEnvironment(objectives, var_ranges, settingsGA, function, output)
    env.run()
else:
    function.slaves_work()
