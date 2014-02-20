from random import random, choice, randrange, randint
from math import log

class Individual(object):

    def __init__(self):
        self.chromosome = {}
        self.objectives = {} # dict with objectives values
        self.optimization = 'minimization'
        self.rank = None # Pareto Front Rank

    def make_chromosome(self):
        pass

    def crossover(self,other):
        pass

    def mutation(self):
        pass

    def dominate(self, other):
        a = False
        for obj_name in self.objectives.keys(): # smaller means better
            if self.objectives[obj_name] > other.objectives[obj_name]: return False
            if self.objectives[obj_name] < other.objectives[obj_name]: a = True
        return a

    def __eq__(self, other):
        for obj_name in self.objectives.keys():
            if self.objectives[obj_name] == other.objectives[obj_name]: a = True
            else: return False
        for var_name in self.chromosome.keys():
            if self.chromosome[var_name] == other.chromosome[var_name]: a = True
            else: return False
        return a
        
    def score(self):
        names = self.objectives.keys()
        try:
            names[1]
            score = self.rank
        except:
            score = self.objectives[names[0]]
        return score

    def __cmp__(self, other):
        if self.optimization == 'minimization':
            return cmp(self.score(), other.score())
        if self.optimization == 'maximization':
            return cmp(other.score(), self.score())

class BinaryCoded(Individual):
    def __init__(self, var_ranges):
        Individual.__init__(self)
        self.var_ranges = var_ranges
        self.var_names = [name for name in self.var_ranges]
        self.accuracy = 3
        self.num_genes = {}
        for var_name in self.var_names:
            low = self.var_ranges[name][0]
            high = self.var_ranges[name][1]
            self.num_genes[var_name] = int(self.accuracy*log(10)/log(2)+log(high - low)/log(2)) + 1
        self.bin_chromosome = {}
        self.make_chromosome()
    
    def make_chromosome(self):
        for var_name in self.var_names:
            num_genes = self.num_genes[var_name]
            chromosome = [randint(0,1) for g in range(num_genes)]
            self.bin_chromosome[var_name] = chromosome
        self.update_real_chromosome()

    def update_real_chromosome(self):
        tmp = ''
        for var_name in self.var_names:
            bin_chromosome = self.bin_chromosome[var_name]
            num_genes = self.num_genes[var_name]
            bin_str = tmp.join(str(gene) for gene in bin_chromosome)
            real_chromosome = (int(bin_str, 2) - pow(2, num_genes - 1))/pow(10.0, self.accuracy)
            self.chromosome[var_name] = real_chromosome

    def mutation(self):
        mutated_var = choice(self.var_names)
        num_genes = self.num_genes[mutated_var]
        mutated_gene = randrange(0, num_genes)
        if self.bin_chromosome[mutated_var][mutated_gene] == 0:
            self.bin_chromosome[mutated_var][mutated_gene] = 1 # bit flip
        else:
            self.bin_chromosome[mutated_var][mutated_gene] = 0 # bit flip
        self.update_real_chromosome()


    def crossover(self, other, crossover_type='two-points'):
        child = self.__class__(self.var_ranges)
        if crossover_type=='two-points':
            return self.two_points_cross(other, child)
    
    def two_points_cross(self, other, child):
        for name in self.var_names:
            num_genes = self.num_genes[name]
            left = randrange(1, num_genes - 2)
            right = randrange(left, num_genes - 1)
            tmp_chromosome = self.bin_chromosome[name]
            other_chromosome = other.bin_chromosome[name]
            tmp_chromosome[left:right] = other_chromosome[left:right]
            child.bin_chromosome[name] = tmp_chromosome
        child.update_real_chromosome()
        return child
    
    def copy(self): # makes copy of individual
        twin = self.__class__(self.var_ranges)
        twin.chromosome = self.chromosome
        twin.bin_chromosome = self.bin_chromosome
        twin.objectives = self.objectives
        twin.rank = self.rank
        return twin

class RealCoded(Individual):

    def __init__(self, gene_ranges):
        Individual.__init__(self)
        self.gene_ranges = gene_ranges # dictionary
        self.gene_names = [name for name in self.gene_ranges]
        self.make_chromosome()
        

    def make_chromosome(self):
        for name in self.gene_names:
            min = self.gene_ranges[name][0]
            max = self.gene_ranges[name][1]
            self.chromosome[name] = min + (max - min)*random()
    
    def adjust_ranges(self):#adjust genes to given ranges
        for name in self.gene_names:
            ranges = self.gene_ranges[name]
            if self.chromosome[name] > ranges[1]:
                self.chromosome[name] = ranges[1]
            if self.chromosome[name] < ranges[0]:
                self.chromosome[name] = ranges[0]

    def crossover(self, other, crossover_type='BLXa'):
        child = self.__class__(self.gene_ranges)
        if crossover_type == 'flat':
            return self.flatCrossover(other,child)
        if crossover_type == 'BLXa':
            return self.BLXa_crossover(other,child)

    def BLXa_crossover(self, other, child, alpha=0.5):
        for name in self.gene_names:
            gene = self.chromosome[name]
            if gene > other.chromosome[name]:
                Cmax = gene
                Cmin = other.chromosome[name]
            else:
                Cmin = gene
                Cmax = other.chromosome[name]
            I = Cmax - Cmin
            UpLim = Cmax + I*alpha
            DownLim = Cmin - I*alpha
            child.chromosome[name] = DownLim + (UpLim - DownLim)*random()
        child.adjust_ranges()
        return child

    def flat_crossover(self, other, child):
        return self.BLXa_crossover(other, child, alpha=0.0)

    def mutation(self, mutation_type='random'):
        if mutation_type == 'random':
            self.random_mutation()

    def random_mutation(self):
        mutated_gene = choice(self.gene_names)
        min = self.gene_ranges[mutated_gene][0]
        max = self.gene_ranges[mutated_gene][1]
        self.chromosome[mutated_gene] = min + (max - min)*random()

    def copy(self): # makes copy of individual
        twin = self.__class__(self.gene_ranges)
        twin.chromosome = self.chromosome
        twin.objectives = self.objectives
        twin.rank = self.rank
        return twin
 

