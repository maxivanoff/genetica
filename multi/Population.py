from genetica.common import Population

class VEGAPopulation(Population.CommonPopulation):
    """
    Vector Evaluated Genetic Algorithm (VEGA)
    """
    def __init__(self, individual=None, size=None, cross_rate=None, mut_rate=None, var_ranges=None, objectives=None):
        Population.CommonPopulation.__init__(self, individual=individual, size=size, cross_rate=cross_rate, mut_rate=mut_rate, var_ranges=var_ranges, objectives=objectives)
        self.subpop_size = self.size/self.num_objectives
        self.subpops=[]
        for _ in self.objectives:
            self.subpops.append([])
    
    def combine_subpops(self):
        population = []
        for subpop in self.subpops:
            population += subpop
        self.individuals = population[:]
    
    def get_subpops(self):
        i=0
        for obj in self.objectives:
            subpop = self.select_proportionally(obj)
            self.subpops[i] = subpop[:]
            i+=1
    
    def select_proportionally(objective):
        subpop=[]
        for i in range(self.subpop_size):
            subpop += self.select(objective=objective, selection_type='Proportional Selection')
        return subpop

    def evolve(self):
        self.get_subpops()
        self.combine_subpops()
        self.crossover()
        
    def crossover(self):
        while len(next_population) < self.size:
            mate1 = self.select(objective=None, selection_type='Random')
            offspring = self.common_crossover(mate1=mate1, selection_type='Random')
            self.common_mutation(offspring)
            next_population.append(offspring)
        self.individuals = next_population[:]


