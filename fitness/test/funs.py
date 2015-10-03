import numpy as np

delta = 0.5
s = 8.
a = 0.05
v = 0.7

def two_min(individual):
    X = individual.chromosome['x']
    Y = individual.chromosome['y']
    R = (a*(X-s)**2 + delta - a*X*X)**2 + 4*v*v
    Z = (a*(X-s)**2 + delta + a*X*X - np.sqrt(R))*0.5 - 0.5*(a*s*s + delta - np.sqrt((a*s*s + delta)**2 + 4*v*v)) + 0.05*Y*Y
    individual.objectives['Z'] = Z

def quadratic(individual):
    x1 = individual.chromosome['X1']
    score = (x1-2)**2
    individual.objectives['objective2'] = score
        

def localglobal(objective, chromosome):
    x1 = chromosome['X1']
    x2 = chromosome['X2']
    if objective=='objective1':
        score = np.sin(np.pi/2.*x1)
    if objective=='objective2':
        score =(1 - np.exp(-(x2 - self.a1)**2/self.b1)) + (1 - 0.5*np.exp(-(x2 - self.a2)**2/self.b2))
        score = score/np.arctan(100*x1)
    return score
