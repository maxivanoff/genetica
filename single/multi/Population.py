from genetica.common import Population

class VEGAPopulation(Population.CommonPopulation):
    """
    Vector Evaluated Genetic Algorithm (VEGA)
        
    Entire population is splitted into K subpopulations. K is number of objectives.
    Each subpopulation is filled up with solutions selected proportionally 
    with respect to one of the objectives. Then subpopulations are combined together
    to form new population, on which crossover and mutation are applied

    update() - selects and combines subpopulations 
    evolve() - individuals are selected randomly for mutation and crossover
    """
    def __init__(self, individual=None, size=None, cross_rate=None, mut_rate=None, var_ranges=None, objectives=None):
        Population.CommonPopulation.__init__(self, individual=individual, size=size, cross_rate=cross_rate, mut_rate=mut_rate, var_ranges=var_ranges, objectives=objectives)
        subsize = self.size/self.num_objectives
        self.subsizes = self.num_objectives*[subsize]
        self.subsizes[0] += self.size%self.num_objectives
        self.subpops=[]
        for _ in self.objectives:
            self.subpops.append([])
    
    def get_subpops(self):
        i=0
        for obj in self.objectives:
            subpop = self.select_proportionally(obj,i)
            self.subpops[i] = subpop[:]
            i+=1
    
    def select_proportionally(self, objective, obj_ind):
        subpop=[]
        for i in range(self.subsizes[obj_ind]):
            subpop += [self.select(objective=objective, selection_type='Proportional Selection')]
        return subpop
    
    def combine_subpops(self):
        population = []
        for subpop in self.subpops:
            population += subpop
        self.individuals = population[:]
    
    def update(self):
        self.get_subpops()
        self.combine_subpops()
        
    def evolve(self):
        next_population=[]
        while len(next_population) < self.size:
            mate1 = self.select(objective=None, selection_type='Random')
            offspring = self.common_crossover(mate1=mate1, selection_type='Random')
            self.common_mutation(offspring)
            next_population.append(offspring)
        self.individuals = next_population[:]

    def best(self):
        return self.individuals


class RDGAPopulation(Population.CommonPopulation):
    class RDGrid:
        def __init__(self):
            pass
        def update(self):
            pass
 
    def __init__(self, individual=None, size=None, cross_rate=None, mut_rate=None, var_ranges=None, objectives=None):
        Population.CommonPopulation.__init__(self, individual=individual, size=size, cross_rate=cross_rate, mut_rate=mut_rate, var_ranges=var_ranges, objectives=objectives)
        self.RDgrid = RDGrid()


