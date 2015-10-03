from results import Results
import logging
import os
env_logger = logging.getLogger('genetica.Environment')

class CommonEnvironment(object):
    """
    Defines all necessary attributes and methods to support the algorithm without actual implementation of the algorithm.
    
    step() defines the actual algorithm which is performed at each generation
    """
    def __init__(self, name=None, objectives=None, var_ranges=None, settings=None, Individual=None, Population=None, fitness=None):
        env_logger.info('Creating CommonEnvironment instance\nname: %s' % (name))
        self.name = name
        self.objectives = objectives
        self.num_objectives = len(objectives)
        self.var_ranges = var_ranges
        self.size = settings['size'] 
        self.maxgenerations = settings['maximum generations']
        self.crossover_rate = settings['crossover rate']
        self.mutation_rate = settings['mutation rate']
        self.num_cycles = settings['number GA cycles'] # number of GA repetitions
        self.Individual = Individual
        self.Population = Population
        self.fitness = fitness
        self.best_individuals = []
        self.num_generations = []
        self.times = []
        self.results = []
        self.generation = 0

    def initialize_population(self):
        self.population = self.Population(self.Individual, self.size, self.crossover_rate, self.mutation_rate, self.var_ranges, self.objectives)
        self.fitness.calculation(self.population.individuals) #fitness function calculation for 0 generation
        ##self.population.assign_ranks()
        self.population.collect_statistics() # averaging
        self.save() # write data to logfiles

    
    def run(self):
        for i in range(self.num_cycles):
            env_logger.info('Running %i GA cycle' % i)
            self.results.append(Results())
            self.run_cycle()
        self.fitness.close() # master sends signal to slaves that work is done

    def run_cycle(self):
        self.generation = 0
        self.initialize_population()
        while not self.too_many_generations():
            self.step() # single GA iteration

    def too_many_generations(self):
        return self.generation > self.maxgenerations
    
    def step(self): # algorithm itself
        """
        General algorithm (can be changed)
        Selection, crossover mutation to produce new generation
        Calculation of fitness scores for new generation
        Averaging
        Report
        """
        pass

    def save(self): # this is done each generation
        """
        results = {'best': self.population.best(),
                   'gen': self.generation,
                   'deviations': self.population.deviations,
                   'averages': self.population.averages,
                   'time': self.population.time,
                   'individuals': self.population.individuals,
                   }
        self.results[-1].report(results)
        """
        self.dump_to_file()

    def dump_to_file(self):
        s = ''
        for key in self.population.individuals[0].chromosome.keys():
            s += '%s ' % key
        for key in self.population.individuals[0].objectives.keys():
            s += '%s ' % key
        s += '\n'
        for individ in self.population.individuals:
            for key, value in individ.chromosome.items():
                s += '%.10f ' % value
            for key, value in individ.objectives.items():
                s += '%.10f ' % value
            s += '\n'
        if not os.path.exists('./output'):
            os.system('mkdir ./output')
        if not os.path.exists('./output/%s' % self.name):
            os.system('mkdir ./output/%s' % self.name)
        file = open('./output/%s/%03i.log' % (self.name, self.generation), 'w')
        file.write(s)
        file.close()


