from mpi4py import MPI
import logging, sys

from genetica.single import Environment
from genetica.fitness import FitnessFunction 
from fitness.test import funs
from postprocess import Output

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

logger = logging.getLogger(__name__)
lf = '%(levelname)s: %(funcName)s at %(filename)s +%(lineno)s\n%(message)s\n'
logging.basicConfig(level=logging.INFO, format=lf)

job_name = 'two_min'
settingsGA = {'size': 20,\
                'crossover rate': 0.95,\
                'mutation rate': 0.05,\
                'maximum generations': 15,\
                'number GA cycles': 1}
objectives = ['Z']

var_ranges = {
        'x': [-4., 12.],
        'y': [-6., 6.],
        }

function = FitnessFunction.Parallel(fitness=funs.two_min, comm=comm, total_jobs=settingsGA['size'])

if rank==0:
    env = Environment.SingleEnvironment(job_name, objectives, var_ranges, settingsGA, function)
    env.run()
    o = Output(job_name, var_ranges, objectives, settingsGA)
else:
    function.slaves_work()



