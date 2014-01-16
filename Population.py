import numpy
import time
from random import random, uniform, choice
from copy import deepcopy

class Population(object):

    def __init__(self, individual=None, size=None, crossover_rate=None, mutation_rate=None, var_ranges=None):
        self.individual = individual
        self.size = size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.var_ranges = var_ranges # dictionary
        self.individuals = self.make_population()
        self.averages = {}
        self.deviations = {}
        self.time = None
        self.starting_time = time.time()

    def make_population(self):
        return [self.individual(self.var_ranges) for i in range(self.size)]

    def collect_statistics(self):
        self.time = time.time()-self.starting_time
        scores = [individ.score for individ in self.individuals]
        total_score = numpy.sum(scores)
        for i in range(self.size):
            self.individuals[i].weight = self.individuals[i].score/total_score
        self.deviations['score'] = numpy.std(scores)
        self.averages['score'] = numpy.average(scores)
        for var_name in self.var_ranges:
            values = []
            for individ in self.individuals:
                value = individ.chromosome[var_name]
                values.append(value)
            self.averages[var_name] = numpy.average(values)
            self.deviations[var_name] = numpy.std(values)
     
    def mutation(self, individual):
        rnd_mut = random()
        if rnd_mut < self.mutation_rate:
            individual.mutation()
        else:
            pass # no mutation

    def evolve(self):
        next_population = []
        self.individuals.sort()
        best_chromosome = self.individuals[0].copy()
        next_population.append(deepcopy(best_chromosome)) #save best chromosome
        while len(next_population) < self.size:
            mate1 = self.select()
            if random() < self.crossover_rate:
                mate2 = self.select()
                offspring = mate1.crossover(mate2)
            else:
                offspring = mate1.copy()
            offspring = deepcopy(offspring)
            self.mutation(offspring)
            next_population.append(offspring)
        self.individuals = next_population

    def select(self, selection_type = 'Proportional Selection'):
        if selection_type == 'Proportional Selection':
            return self.proportional_selection()
        if selection_type == 'Tournament':
            return self.tournament()

    def proportional_selection(self):
        competitors=[]
        k=uniform(self.individuals[0].weight, self.individuals[-1].weight)
        for i in range(self.size):
            if self.individuals[i].weight<=k:
                competitors.append(self.individuals[i])
        return choice(competitors)

    def tournament(self, size=8, choosebest=0.90):
        competitors = [choice(self.individuals) for i in range(size)]
        competitors.sort()
        if random() < choosebest:
            return competitors[0]
        else:
            return choice(competitors[1:])


