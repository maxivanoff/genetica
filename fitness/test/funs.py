import numpy as np

def quadratic(objective, chromosome):
    x1 = chromosome['X1']
    if objective=='objective1':
        score = x1**2
    if objective=='objective2':
        score = (x1-2)**2
    return score
        

def localglobal(objective, chromosome):
    x1 = chromosome['X1']
    x2 = chromosome['X2']
    if objective=='objective1':
        score = np.sin(np.pi/2.*x1)
    if objective=='objective2':
        score =(1 - np.exp(-(x2 - self.a1)**2/self.b1)) + (1 - 0.5*np.exp(-(x2 - self.a2)**2/self.b2))
        score = score/np.arctan(100*x1)
    return score
