from genetica.common import Environment, Individual
from genetica.single import Population

class SingleEnvironment(Environment.CommonEnvironment):

    def __init__(self, name=None, objectives=None, var_ranges=None, settings=None, fitness=None):
        Individ = Individual.RealCoded
        Pop = Population.SinglePopulation
        Environment.CommonEnvironment.__init__(self, name=name, objectives=objectives, var_ranges=var_ranges, settings=settings, Individual=Individ, Population=Pop, fitness=fitness)

    def initialize_population(self):
        self.population = self.Population(self.Individual, self.size, self.crossover_rate, self.mutation_rate, self.var_ranges, self.objectives)
        self.fitness.calculation(self.population.individuals) #fitness function calculation for 0 generation
        self.population.update()
        self.population.collect_statistics() # averaging
        self.save() # write data to logfiles
    
    
    def step(self): # algorithm itself
        self.generation += 1
        self.population.evolve() # select, breed, mutate => new generation
        self.fitness.calculation(self.population.individuals) # fitness function calculation of next gen
        self.population.update()
        self.population.collect_statistics() # averaging
        self.save() # write data to logfiles




