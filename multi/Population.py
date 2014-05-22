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
            subpop = self.select_subpop(obj,i,'Proportional Selection')
            self.subpops[i] = subpop[:]
            i+=1
    
    def select_subpop(self, objective, obj_ind, selection_type):
        subpop=[self.select(objective, selection_type)]
        while len(subpop) < self.subsizes[obj_ind]:
            selected = self.select(objective, selection_type)
            if not selected in subpop: 
                subpop += [selected]
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


class IndividualsContainer(object):
    """
    In progress...
    Move to commnon once is done.
    """
    def __init__(self, individuals_list):
        self.container = individuals_list
        self.objective_names = self.container[0].objectives.keys()

    def __iter__(self):
        return iter(self.container)

    def get_maxscore(self, objective):
        pass
    def get_minscore(self, objective):
        pass
    def assign_ranks(self):
        pass

class RDGAPopulation(Population.CommonPopulation):
    """
    In progress...
    """
    
    class ObjectiveSpace:
        def __init__(self, individuals):
            self.individuals = individuals
            self.dimensions_names = self.individuals.objective_names
            self.dimensionality = len(self.dimensions_names)
            self.cell_size = {}
            self.grid_size = {}
            self.minmax = {}
            self.update()
            self.define_cell_signatures()

        #def define_cell_signatures(self):
        #    for i in range(cells_number):
                

        def update(self):
            cells_number = self.dimensionality*[10] # number of cells in each dimension
            for objective, K in zip(self.dimensions_names, cells_number):
                fmax = self.individuals.get_maxscore(objective)
                fmin = self.individuals.get_minscore(objective)
                self.grid_size[objective] = fmax - fmin
                self.minmax[objective] = (fmin, fmax)
                self.cell_size = self.grid_size[objective]/K

        def assign_densities(self):
            # assign coordinates
            for individ in self.individuals:
                for objective in self.dimensions_names:
                    obj_value = individ.objectives[objective]
                    crd = int((obj_value - self.minmax[objective][0])/self.cell_size[objective])
                    individ.coordinates[objective] = crd

 
    def __init__(self, individual=None, size=None, cross_rate=None, mut_rate=None, var_ranges=None, objectives=None):
        Population.CommonPopulation.__init__(self, individual=individual, size=size, cross_rate=cross_rate, mut_rate=mut_rate, var_ranges=var_ranges, objectives=objectives)
        self.individuals = IndividualsContainer(self.individuals)
        self.grid = ObjectiveSpace(self.individuals)


