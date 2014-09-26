from genetica.common import Population
from copy import deepcopy

class SinglePopulation(Population.CommonPopulation):
    
    def __init__(self, individual=None, size=None, cross_rate=None, mut_rate=None, var_ranges=None, objectives=None):
        Population.CommonPopulation.__init__(self, individual=individual, size=size, cross_rate=cross_rate, mut_rate=mut_rate, var_ranges=var_ranges, objectives=objectives)
        self.objective = self.objectives[0] # first in the list is optimized
    
    def update(self):
        self.individuals = sorted(self.individuals, key=lambda ind: ind.objectives[self.objective])

    def evolve(self):
        next_population=self.best()
        while len(next_population) < self.size:
            mate1 = self.select(self.objective, selection_type='Proportional Selection')
            offspring = self.common_crossover(mate1, self.objective, selection_type='Proportional Selection')
            self.common_mutation(offspring)
            next_population.append(offspring)
        self.individuals = next_population[:]

    def best(self):
        return [deepcopy(self.individuals[0])]



