import os
import csv
import numpy as np
import itertools
try:
    from scipy.optimize import curve_fit
except ImportError:
    pass
try:
    import matplotlib.pyplot as plt
    graphics = True
except:
    graphics = False

class Output(object):

    def __init__(self, problem_name=None, objectives=None, results=None, plot_ranges=None, var_ranges=None, settings=None, plot=True):
        self.problem_name = problem_name
        if objectives is None:
            self.objectives = []
        else:
            self.objectives = objectives
        self.num_objectives = len(self.objectives)
        self.results = results
        self.plot_ranges = plot_ranges ## dictionary, it has names of variables
        self.var_ranges = var_ranges
        if not self.problem_name is None:
            if not os.path.exists('./output'):
                os.system('mkdir ./output')
            self.main_output = './output/%s' % (self.problem_name)
            if os.path.exists(self.main_output):
                os.system('rm -r %s' % (self.main_output))
            os.system('mkdir %s' % (self.main_output))
            self.raw_output = '%s/raw' % (self.main_output)
            os.system('mkdir %s' % (self.raw_output))
            self.save_details()
            self.dump_info(settings) # save info about GA settings
        else:
            self.main_output = None
        if graphics and plot:
            self.graphics = True
        else:
            self.graphics = False
    
    def write_logfiles(self):
        for i, res in enumerate(self.results):
            output_dir = '%s/%i' % (self.main_output, i)
            os.system('mkdir %s' % (output_dir) )
            self.conv_log = open('%s/convergence.log' % (output_dir),'w')
            self.stats_log = open('%s/statistics.log' % (output_dir),'w')
            self.write_header() # line with titles in outfile
            self.conv_str = ''
            self.stats_str = ''
            for gen in range(len(res.generations)):
                individ = res.best[gen][0]
                self.conv_str += '%i ' % (gen)
                # report objective values
                for obj_name in self.objectives:
                    value = individ.objectives[obj_name]
                    self.conv_str += '%.8f ' % (value)
                # report variables values
                for var_name in self.var_ranges:
                    value = individ.chromosome[var_name]
                    self.conv_str += '%.8f ' % (value)
                self.conv_str += '\n'     
                # report stats at the current generation
                self.stats_str += '%i ' % (gen)
                for objective in self.objectives:
                    self.stats_str += '%.8f ' % (res.averages[gen][objective])
                    self.stats_str += '%.8f ' % (res.deviations[gen][objective])
                for var_name in self.var_ranges:
                    self.stats_str += '%.8f ' % (res.averages[gen][var_name])
                    self.stats_str += '%.8f ' % (res.deviations[gen][var_name])
                self.stats_str += '%.1f\n' % (res.times[gen])
            self.conv_log.write(self.conv_str)
            self.stats_log.write(self.stats_str)
            self.conv_log.close()
            self.stats_log.close()
    
    def write(self):
        # convergence logs
        self.write_logfiles()
        # analyses of the best solutions
        best_individuals = [res.best[-1][0] for res in self.results]
        self.num_solutions = len(best_individuals)
        data = self.convert_to_data(best_individuals)
        self.stats(data)
        if self.graphics:
            self.correlate_pairs(data)
            self.build_histograms(data)
        self.save_data(data)
    
    def stats(self, data):
        generations = [res.generations[-1] for res in self.results]
        times = [res.times[-1] for res in self.results]
        self.statsfile = open('%s/stats' % (self.main_output), 'w')
        self.stats_convergence(data, generations, times)
        self.stats_variables(data)
        self.statsfile.close()
     
    def correlate_pairs(self, data, plot_ranges=None, objectives=None, output=None):
        if plot_ranges: self.plot_ranges = plot_ranges
        if objectives: self.objectives = objectives
        if output: self.main_output = './%s/' % (output)
        pairs = itertools.combinations(data.keys(), 2)
        stats = {}
        for pair in pairs:
            if pair[0] in self.objectives:
                Yname = pair[0]
                Xname = pair[1]
            elif pair[1] in self.objectives:
                Yname = pair[1]
                Xname = pair[0]
            else:
                pair = sorted(pair)
                Yname = pair[0]
                Xname = pair[1]
            x = data[Xname]
            y = data[Yname]
            if Xname in self.plot_ranges: xlim = self.plot_ranges[Xname]
            else: xlim = [min(x), max(x)]
            if Yname in self.plot_ranges: ylim = self.plot_ranges[Yname]
            else: ylim = [min(y), max(y)]
            plt.grid(True)
            plt.xlabel(Xname)
            plt.ylabel(Yname)
            plt.ylim(ylim)
            plt.xlim(xlim)
            correlation = np.corrcoef(x,y)[0,1]
            R2 = correlation**2
            if R2 > 0.30 and not Xname in self.objectives and not Yname in self.objectives:
                popt, pcov = curve_fit(lambda xdata,m,n: m*xdata+n, np.array(x), np.array(y))
                a, b = popt
                da, db = np.sqrt(np.diag(pcov))
                xx = np.arange(xlim[0], xlim[1], 0.01)
                yy = a*xx + b
                plt.plot(xx, yy, '--', color='black', linewidth=3, label='%s = %.3f(%.3f)*%s + %.3f(%.3f)\nR2 = %.2f' % (Yname, a, da, Xname, b, db, R2))
                plt.legend(loc='upper right')
                stats['%s-%s' % (Yname, Xname)] = [a, da, b, db, R2]
            plt.plot(x, y, 'ro', ms=7.5)
            filename = self.main_output + '/%s-%s.pdf' % (Yname, Xname)
            plt.savefig(filename)
            plt.close()
        return stats
    
    def build_histograms(self, data):
        for key, values in data.items():
            plt.grid(True)
            plt.xlabel(key)
            plt.yticks([])
            n, bins, patches = plt.hist(values, 15, normed=1, facecolor='green', alpha=0.75)
            filename = self.main_output + '/%s.pdf' % (key)
            plt.savefig(filename)
            plt.close()
    
    def write_header(self):
        #convergence.log
        reportstr = 'gen '
        for objective in self.objectives:
            reportstr += '%s ' % (objective)
        for var_name in self.var_ranges:
            reportstr += '%s ' % (var_name)
        self.conv_log.write(reportstr+'\n')
        # statistics.log        
        reportstr = 'gen '
        for objective in self.objectives:
            reportstr += 'ave_%s ' % (objective)
            reportstr += 'std_%s ' % (objective)
        for var_name in self.var_ranges:
            reportstr += 'ave_%s ' % (var_name)
            reportstr += 'std_%s ' % (var_name)
        reportstr += 'time\n'
        self.stats_log.write(reportstr)
    
    
    def stats_convergence(self, data, generations, times):
        if self.num_objectives == 1:
            s = 'BEST SOLUTION\n'
            self.statsfile.write(s)
            for objective in self.objectives:
                best_index = data[objective].index(min(data[objective]))
            for var_name in self.plot_ranges:
                value = data[var_name][best_index]
                s = '%s: %.8f\n' % (var_name, value)
                self.statsfile.write(s)
        if self.num_objectives > 1:
            s = 'BEST SOLUTIONS: %i solutions\n' % (self.num_solutions)
            self.statsfile.write(s)
            for i in range(self.num_solutions):
                for objective in self.objectives:
                    s = '%s: %.8f\n' % (objective, data[objective][i])
                    self.statsfile.write(s)
                for var_name in self.plot_ranges:
                    s = '%s: %.8f\n' % (var_name, data[var_name][i])
                    self.statsfile.write(s)
                s = '--------------------\n'
                self.statsfile.write(s)

        for objective in self.objectives:
            s = '\n%s\n' % (objective)
            self.statsfile.write(s)
            scores = data[objective]
            s = 'lowest: %.8f highest: %.8f average: %.8f median: %.8f std: %.8f\n' % (np.amin(scores), np.amax(scores), np.average(scores), np.median(scores), np.std(scores))
            self.statsfile.write(s)
        
        s = '\nGENERATIONS\n'
        self.statsfile.write(s)
        s = 'lowest: %i highest: %i average: %.1f median: %.1f std: %.1f\n\n' % (np.amin(generations), np.amax(generations), np.average(generations), np.median(generations), np.std(generations))
        self.statsfile.write(s)
        
        s = '\nTIMES\n'
        self.statsfile.write(s)
        s = 'lowest: %.3f highest: %.3f average: %.3f median: %.3f std: %.3f\n\n' % (np.amin(times), np.amax(times), np.average(times), np.median(times), np.std(times))
        self.statsfile.write(s)

    def stats_variables(self, data):
        s = 'VARIABLES\n'
        self.statsfile.write(s)
        for var_name in self.plot_ranges:
            s = 'variable name: %s\n' % (var_name)
            self.statsfile.write(s)
            s = 'lowest: %.8f highest: %.8f average: %.8f median: %.8f std: %.8f\n\n' % (np.amin(data[var_name]), np.amax(data[var_name]), np.average(data[var_name]), np.median(data[var_name]), np.std(data[var_name]))
            self.statsfile.write(s)
    
    def dump_info(self, settings):
        size = settings['size']
        crossrate = settings['crossover rate']
        mutrate = settings['mutation rate']
        maxgen = settings['maximum generations']

        infofile = open('%s/info' % (self.main_output), 'w')
        s = 'Objectives: '
        for objective in self.objectives:
            s += '%s ' % (objective)
        infofile.write(s + '\n')
        s = 'Maximum generations: %i\n' % (maxgen)
        infofile.write(s)
        s = 'Population size: %i\n' % (size)
        infofile.write(s)
        s = 'Crossover rate: %.3f\n' % (crossrate)
        infofile.write(s)
        s = 'Mutation rate: %.3f\n' % (mutrate)
        infofile.write(s)
        infofile.close()
    def convert_to_data(self, best_individuals):
        data = {}
        for var_name in self.plot_ranges:
            data[var_name] = [individ.chromosome[var_name] for individ in best_individuals]
        for obj_name in self.objectives:
            data[obj_name] = [individ.objectives[obj_name] for individ in best_individuals]
        return data
        
    def save_data(self, data):
        file = open('%s/solutions.csv' % (self.raw_output), 'wb') 
        writer = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key, value in data.items():
            writer.writerow([key])
            writer.writerow(value)
        file.close()
    
    def save_details(self):
        file = open('%s/details.csv' % (self.raw_output), 'wb') 
        writer = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key, value in self.plot_ranges.items():
            writer.writerow([key])
            writer.writerow(value)
        file.close()
    
    def read_data(self, name=None):
        if name is None:
            name = self.problem_name
        file = open('%s/raw/solutions.csv' % (name), 'r')
        i=0
        data={}
        for line in file:
            if not i%2: 
                tmp = line.strip().split('|')
                if len(tmp)>1: name = tmp[1]
                else: name = tmp[0]
                data[name] = []
            else:
                data[name] = np.array([float(t) for t in line.split()])
            i+=1
        file.close()
        return data
    
    def read_details(self):
        reader = csv.reader(open('details.csv', 'rb'))
        i = 0
        data = {}
        for line in reader:
            if i%2: name = line.split()
            else: 
                value = list(line.split())
                data[name] = value
        return data


