import numpy as np
from genetica import FitnessFunction


class Fitness(FitnessFunction.ParallelFitness):
    def __init__(self,  problem_name, fit_prms=0, comm=None, size=None):
        FitnessFunction.ParallelFitness.__init__(self,comm, size)
        angle = fit_prms/180.0*np.pi
        self.R = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])

    def get_score(self, chromosome):
        vector = []
        for var_name in chromosome:
            value = chromosome[var_name]
            vector.append(value)
        vector=np.array(vector)
        Rvector = np.dot(self.R,vector)
        x = Rvector[0]
        y = Rvector[1]
        self.score = 0.1*pow(x,2) + abs(y)
        return self.score

