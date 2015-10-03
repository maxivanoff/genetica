from genetica.single import Environment
from genetica.fitness import FitnessFunction 
from fitness.test import funs
import logging, sys
from postprocess import Output
logger = logging.getLogger(__name__)
lf = '%(levelname)s: %(funcName)s at %(filename)s +%(lineno)s\n%(message)s\n'
logging.basicConfig(level=logging.INFO, format=lf)

job_name = 'two_min'
settingsGA = {'size': 20,\
                'crossover rate': 0.95,\
                'mutation rate': 0.05,\
                'maximum generations': 15,\
                'number GA cycles': 1}
# Objectives, all will be plotted at the end, but the first one will be optimized
objectives = ['Z']

# if coordinates are set to multipoles, number of multipoles must be equal to number of variables

#var_ranges = ChargeRanges(coordinates, molecules.sites_names, multipoles)
#fitness = GACharges(molecules=molecules, coordinates=coordinates, charge_constraint=Qc) 
#function = FitnessFunction.Single(fitness.fitness)
var_ranges = {
        'x': [-4., 12.],
        'y': [-6., 6.],
        }

function = FitnessFunction.Single(funs.two_min)

env = Environment.SingleEnvironment(job_name, objectives, var_ranges, settingsGA, function)
env.run()

o = Output(job_name, var_ranges, objectives, settingsGA)

#output = Output.Output(problem_name=job_name, objectives=objectives,\
#        results=env.results, plot_ranges=var_ranges, settings=settingsGA,\
#        var_ranges=var_ranges) 
#output.write()

