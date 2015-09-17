from genetica.common import Output
from genetica.single import Environment
from genetica.fitness import FitnessFunction 
from fftoolbox.ChargeOptimizer import GACharges
from fftoolbox.GridMolecules import MoleculeOnGridList
from fftoolbox.ranges import ChargeRanges, PlotRanges
from fftoolbox.convert import Convert
from fftoolbox.forcefield import TIP5P
import pickle
import logging, sys
logger = logging.getLogger(__name__)
lf = '%(levelname)s: %(funcName)s at %(filename)s +%(lineno)s\n%(message)s\n'
logging.basicConfig(level=logging.INFO, format=lf)

molecule_name = 'chloromethane'
conformations = None
symmetry = True

# only theory=b3lyp; basis=augccpvdz and linear density=1.5 are now available
# 'exclude': ['<xy'] will include only point with positive z
# 'include': ['yz'] - only yz plane is included

g_set = {'theory': 'b3lyp',\
             'basis': 'augccpvdz',\
             'density': 1.5,\
             'exclude': ['outside'],\
             'extension': 'cub'}

settingsGA = {'size': 20,\
                'crossover rate': 0.9,\
                'mutation rate': 0.03,\
                'maximum generations': 100,\
                'number GA cycles': 10}
#total charge constriant
Qc = None

# Objectives, all will be plotted at the end, but the first one will be optimized
objectives = ['esp']

# if coordinates are set to multipoles, number of multipoles must be equal to number of variables
coordinates = 'charges'
multipoles = ['total charge', 'dipole']
molecules = MoleculeOnGridList(name=molecule_name, m_settings=g_set, g_settings=g_set, sym=symmetry)  

var_ranges = ChargeRanges(coordinates, molecules.sites_names, multipoles)
fitness = GACharges(molecules=molecules, coordinates=coordinates, charge_constraint=Qc) 
function = FitnessFunction.Single(fitness.fitness)

env = Environment.SingleEnvironment(objectives, var_ranges, settingsGA, function)
env.run()
Convert(results=env.results, molecules=molecules, coordinates=coordinates)

plot_ranges = PlotRanges(var_ranges)

output = Output.Output(problem_name=molecule_name, objectives=objectives,\
        results=env.results, plot_ranges=plot_ranges, settings=settingsGA,\
        var_ranges=var_ranges) 
output.write()
pickle.dump( env.results, open( "./output/%s/results.p" % molecule_name, "wb" ) )

