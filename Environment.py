
class Environment(object):

    def __init__(self, objectives=None, var_ranges=None, size=None, maxgenerations=None, threshold=None, conv_gen=None, crossover_rate=None, mutation_rate=None, num_cycles=None, Individual=None, Population=None, fitness=None, output=None):
        self.objectives = objectives
        self.num_objectives = len(objectives)
        self.var_ranges = var_ranges
        self.size = size
        self.maxgenerations = maxgenerations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.num_cycles = num_cycles # number of GA repetitions
        self.threshold = threshold
        self.conv_gen = conv_gen
        self.Individual = Individual
        self.Population = Population
        self.fitness = fitness
        self.last_best_scores = []
        self.best_individuals = []
        self.num_generations = []
        self.times = []
        self.output = output

    def initialize_population(self):
        self.population = self.Population(self.Individual, self.size, self.crossover_rate, self.mutation_rate, self.var_ranges, self.objectives)
        self.fitness.calculation(self.population.individuals) #fitness function calculation for 0 generation
        self.population.assign_ranks()
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
        self.best_individuals += self.population.elite

    def too_many_generations(self):
        return self.generation > self.maxgenerations
    
    def step(self): # algorithm itself
        self.population.evolve() # select, breed, mutate => new generation
        self.fitness.calculation(self.population.individuals) # fitness function calculation of next gen
        self.assign_ranks()
        self.population.collect_statistics() # averaging
        self.report() # write data to logfiles
        self.generation += 1

    def report(self): # this is done each generation
        elite = self.population.save_elite()
        self.output.write_log(elite, self.generation, self.population.deviations, self.population.averages, self.population.time)


