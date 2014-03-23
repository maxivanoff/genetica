import numpy as np
from genetica.fitness import FitnessFunction

class Fitness(FitnessFunction.ParallelFitness):

    def __init__(self,  problem_name, objectives, fit_prms=0, comm=None, size=None):
        FitnessFunction.ParallelFitness.__init__(self,comm, size)
        self.objectives = objectives

    def f(self,objective, chromosome):
        x1 = chromosome['X1']
        if objective=='objective1':
            score = x1**2
        if objective=='objective2':
            score = (x1-2)**2
        return score
        
    
    def get_scores(self, chromosome):
        scores=[]
        for objective in self.objectives:
            scores.append(self.f(objective, chromosome))
        objectives = dict((o, s) for o,s in zip(self.objectives, scores))
        return objectives

