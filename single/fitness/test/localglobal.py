import numpy as np
from genetica.fitness import FitnessFunction

class Fitness(FitnessFunction.ParallelFitness):

    def __init__(self,  problem_name, objectives, fit_prms=0, comm=None, size=None):
        FitnessFunction.ParallelFitness.__init__(self,comm, size)
        self.objectives = objectives
        self.a1 = 0.1 # defines global min
        self.a2 = 0.8 # defines local min
        self.b1 = 0.0001
        self.b2 = 0.8

    def f(self,objective, chromosome):
        x1 = chromosome['X1']
        x2 = chromosome['X2']
        if objective=='objective1':
            score = np.sin(np.pi/2.*x1)
        if objective=='objective2':
            score =(1 - np.exp(-(x2 - self.a1)**2/self.b1)) + (1 - 0.5*np.exp(-(x2 - self.a2)**2/self.b2))
            score = score/np.arctan(100*x1)
        return score
        
    
    def get_scores(self, chromosome):
        scores=[]
        for objective in self.objectives:
            scores.append(self.f(objective, chromosome))
        objectives = dict((o, s) for o,s in zip(self.objectives, scores))
        return objectives

