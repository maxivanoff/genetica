import numpy as np
from genetica.common import FitnessFunction


class Fitness(FitnessFunction.ParallelFitness):
    def __init__(self,  problem_name, objectives, fit_prms=0, comm=None, size=None):
        FitnessFunction.ParallelFitness.__init__(self,comm, size)
        self.objectives = objectives
        angle = fit_prms/180.0*np.pi
        self.R = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])

    def get_scores(self, chromosome):
        vector = []
        for var_name in chromosome:
            value = chromosome[var_name]
            vector.append(value)
        vector=np.array(vector)
        Rvector = np.dot(self.R,vector)
        x = Rvector[0]
        y = Rvector[1]
        scores = []
        scores.append(0.1*pow(x,2) + abs(y))
        scores.append(0.05*pow(x-y,2) + abs(x+y))
        obj = dict((o, s) for o,s in zip(self.objectives, scores))
        return obj

