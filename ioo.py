import numpy
import itertools
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from genetica import IO

class Output(IO.Output):
    def __init__(self, problem_name, var_ranges):
        IO.Output.__init__(self, problem_name, var_ranges)

    def write_final(self, best_individuals, generations,times):
        self.stats(best_individuals, generations, times)
        self.final_graphical_data(best_individuals)
    
    def stats(self, best_individuals, generations, times):
        IO.Output.stats_convergence(self, best_individuals, generations, times)
        chromosomes = [individ.chromosome for individ in best_individuals]
        IO.Output.stats_variables(self, chromosomes)
        self.statsfile.close()
    
    def final_graphical_data(self, best_individuals):
        filename = '%s/../' % (self.OutputDirName)
        chromosomes = [individ.chromosome for individ in best_individuals]
        scores = [individ.score for inidivid in best_individuals]
        self.correlate_pairs(best_individuals, filename)
        self.build_histogramms(scores, filename, 'score')
        for var_name in chromosomes[0]:
            self.build_histogramms(chromosomes, filename, var_name)
    
    def build_histogramms(self, chromosomes,filename, type):
        data = []
        if type=='score':## here chromosomes are not actual chromosomes, but just scores
            data = chromosomes
        else:
            for chromosome in chromosomes:
                data.append(chromosome[type])
        plt.grid(True)
        plt.xlabel(type)
        plt.yticks([])
        n, bins, patches = plt.hist(data, 15, normed=1, facecolor='green', alpha=0.75)
        filename += '%s.pdf' % (type)
        plt.savefig(filename)
        plt.close()

    def correlate_pairs(self, individuals, templatename):
        prms = {}
        var_names = individuals[0].chromosome.keys() 
        for var_name in var_names:
            prms[var_name] = []
            for individ in individuals:
                prms[var_name].append(individ.chromosome[var_name])

        pairs_of_vars = itertools.combinations(var_names,2)
        i=0
        for pair in pairs_of_vars:
            plt.grid(True)
            plt.axis([-1,1,-1,1])
            plt.xlabel(pair[0])
            plt.ylabel(pair[1])
            x = prms[pair[0]]
            y = prms[pair[1]]
            xmax = numpy.amax(x)
            xmin = numpy.amin(x)
            ymax = numpy.amax(y)
            ymin = numpy.amin(y)
            plt.ylim([min(-1, ymin), max(1, ymax)])
            plt.xlim([min(-1, xmin), max(1, xmax)])
            a,b = numpy.polyfit(x,y,1)
            correlation = numpy.corrcoef(x,y)[0,1]
            R2 = correlation**2
            xx = numpy.arange(min(-1,xmin),max(1,xmax),0.01)
            yy = a*xx + b
            plt.plot(xx,yy,'--',color='black',linewidth=3,label='%s = %.4f*%s + %.4f\nR2 = %.2f' % (pair[1], a, pair[0], b, R2))
            plt.plot(x, y, 'ro', ms=7.5)
            plt.legend(loc='upper right')
            filename = templatename + '%s-%s.pdf' % (pair[1], pair[0])
            plt.savefig(filename)
            plt.close()
            i+=1

   

