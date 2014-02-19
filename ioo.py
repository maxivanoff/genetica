import numpy
import itertools
import matplotlib.pyplot as plt

from genetica import IO

class Output(IO.Output):
    def __init__(self, problem_name, objectives, var_ranges, maxgenerations, size, crossrate, mutrate):
        IO.Output.__init__(self, problem_name, objectives, var_ranges, maxgenerations, size, crossrate, mutrate)

    def write_final(self, best_individuals, generations,times):
        self.stats(best_individuals, generations, times)
        self.final_graphical_data(best_individuals)
    
    


   

