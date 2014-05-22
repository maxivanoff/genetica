
class CommonEnvironment(object):
    """
    Defines all necessary attributes and methods to support the algorithm without actual implementation of the algorithm.
    
    step() defines the actual algorithm which is performed at each generation
    """
    def __init__(self, objectives=None, var_ranges=None, settings=None, Individual=None, Population=None, fitness=None, output=None):
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
        self.output = output

    def initialize_population(self):
        self.population = self.Population(self.Individual, self.size, self.crossover_rate, self.mutation_rate, self.var_ranges, self.objectives)
        self.fitness.calculation(self.population.individuals) #fitness function calculation for 0 generation
        ##self.population.assign_ranks()
        self.population.collect_statistics() # averaging
        self.report() # write data to logfiles
    
    def run(self):
        for i in range(self.num_cycles):
            self.output.open_logfiles(i)
            self.run_cycle()
            self.output.close_logfiles()
        self.fitness.close() # master sends signal to slaves that work is done
        self.output.write_final(self.best_individuals, self.num_generations, self.times) # dumps stats

    def run_cycle(self):
        self.generation = 0
        self.initialize_population()
        while not self.too_many_generations():
            self.step() # single GA iteration
        self.num_generations.append(self.generation)
        self.times.append(self.population.time)
        self.best_individuals += self.population.best()

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

    def report(self): # this is done each generation
        self.output.write_log(self.population.best(), self.generation, self.population.deviations, self.population.averages, self.population.time)


