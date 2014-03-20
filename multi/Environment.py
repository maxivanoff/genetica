from genetica.common import Environment
from genetica.multi import Population, Individual

class VEGAEnvironment(Environment.CommonEnvironment):

    def __init__(self, objectives=None, var_ranges=None, size=None, maxgen=None, cross_rate=None, mut_rate=None, num_cycles=None, fitness=None, output=None):
        Individual = Individual.RealCoded
        Population = Population.VEGAPopulation
        CommonEnvironment.__init__(self, objectives=objectives, var_ranges=var_ranges, size=size, maxgen=maxgen, cross_rate=cross_rate, mut_rate=mut_rate, num_cycles=num_cycles, Individual=Individual, Population=Population, fitness=fitness, output=output):

    def initialize_population(self):
        self.population = self.Population(self.Individual, self.size, self.crossover_rate, self.mutation_rate, self.var_ranges, self.objectives)
        self.fitness.calculation(self.population.individuals) #fitness function calculation for 0 generation
        self.population.collect_statistics() # averaging
        self.report() # write data to logfiles
    
    
    def step(self): # algorithm itself
        self.population.evolve() # select, breed, mutate => new generation
        self.fitness.calculation(self.population.individuals) # fitness function calculation of next gen
        self.population.collect_statistics() # averaging
        self.report() # write data to logfiles
        self.generation += 1


