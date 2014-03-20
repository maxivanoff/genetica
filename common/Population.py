import numpy
import time
import random

class CommonPopulation(object):
    """
    Contains attributed and methods that are common for single and objective(s) optimizations
    """
    def __init__(self, individual=None, size=None, cross_rate=None, mut_rate=None, var_ranges=None, objectives=None):
        self.individual = individual
        self.size = size
        self.crossover_rate = cross_rate
        self.mutation_rate = mut_rate
        self.var_ranges = var_ranges # dictionary
        self.objectives = objectives
        self.num_objectives = len(objectives)
        
        self.averages = {}
        self.deviations = {}
        self.time = None
        self.starting_time = time.time()
        
        self.individuals = self.make_population()

    def make_population(self):
        return [self.individual(self.var_ranges) for i in range(self.size)]

    def collect_statistics(self):
        self.time = time.time()-self.starting_time
        # stats for objectives
        for obj_name in self.objectives:
            scores = [individ.objectives[obj_name] for individ in self.individuals]
            self.deviations[obj_name] = numpy.std(scores)
            self.averages[obj_name] = numpy.average(scores)
        # stats for variables
        for var_name in self.var_ranges:
            values = [individ.chromosome[var_name] for individ in self.individuals]
            self.averages[var_name] = numpy.average(values)
            self.deviations[var_name] = numpy.std(values)
     
    def common_mutation(self, individual):
        if random.random() < self.mutation_rate:
            individual.mutation()
        else:
            pass # no mutation
    
    def common_crossover(self, mate1, selection_type='Proportional Selection')
        if random.random() < self.crossover_rate:
            mate2 = self.select(selection_type)
            offspring = mate1.crossover(mate2)
        else:
            offspring = mate1.copy()
        return offspring
    
    def evolve(self):
        pass

    def select(self, objective=None, selection_type='Proportional Selection'):
        if selection_type == 'Random':
            return self.random_selection()
        if selection_type == 'Proportional Selection':
            return self.proportional_selection(objective)
        if selection_type == 'Tournament':
            return self.tournament(objective)

    def random_selection(self):
        return random.choice(self.individuals)

    def proportional_selection(self, objective):
        sorted_individs = sorted(self.individuals, key=lambda ind: ind.objectives[objective])
        rndm = 0
        while not rndm:
            rndm = random.uniform(0., sorted_individs[-1].objectives[objective])
        competitors = []
        for individ in individuals:
            if individ.objectives[objective] <= rndm:
                competitors.append(individ)
        return random.choice(competitors)

    def tournament(self, objective, size=8, choosebest=0.90):
        competitors = [choice(self.individuals) for i in range(size)]
        sorted_competitors = sorted(competitors, key=lambda individ: individ.objectives[objective])
        if random() < choosebest:
            return sorted_competitors[0]
        else:
            return random.choice(sorted_competitors[1:])


