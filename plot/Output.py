import os
import csv
import numpy
import itertools
try:
    import matplotlib.pyplot as plt
    fig=plt.figure()
    fig.clear()
    plt.close()
    display = True
except:
    display = False

class Output(object):

    def __init__(self, problem_name, objectives, var_ranges, maxgenerations, size, crossrate, mutrate, graphics):
        if display and graphics: self.graphics = True
        else: self.graphics = False
        self.problem_name = problem_name
        self.objectives = objectives
        self.num_objectives = len(objectives)
        self.var_ranges = var_ranges ## dictionary, it has names of variables
        if not os.path.exists('./output'):
            os.system('mkdir ./output')
        self.main_output = './output/%s' % (self.problem_name)
        if os.path.exists(self.main_output):
            os.system('rm -r %s' % (self.main_output))
        os.system('mkdir %s' % (self.main_output))
        self.raw_output = '%s/raw' % (self.main_output)
        os.system('mkdir %s' % (self.raw_output))
        self.save_details()
        self.dump_info(maxgenerations, size, crossrate, mutrate)
    
    def write_final(self, best_individuals, generations, times):
        best_individuals.sort() # makes sense for single objective only
        self.num_solutions = len(best_individuals)
        data = self.convert_to_data(best_individuals)
        self.stats(data, generations, times)
        if self.graphics:
            self.correlate_pairs(data)
            self.build_histograms(data)
        self.save_data(data)
 
        
    def correlate_pairs(self, data):
        pairs = itertools.combinations(data.keys(), 2)
        for pair in pairs:
            Xname = pair[0]
            Yname = pair[1]
            x = data[Xname]
            y = data[Yname]
            if Xname in self.var_ranges: xlim = self.var_ranges[Xname]
            else: xlim = [min(x), max(x)]
            if Yname in self.var_ranges: ylim = self.var_ranges[Yname]
            else: ylim = [min(y), max(y)]
            plt.grid(True)
            plt.xlabel(Xname)
            plt.ylabel(Yname)
            plt.ylim(ylim)
            plt.xlim(xlim)
            correlation = numpy.corrcoef(x,y)[0,1]
            R2 = correlation**2
            if R2 > 0.80:
                xx = numpy.arange(xlim[0], xlim[1], 0.01)
                a,b = numpy.polyfit(x, y, 1)
                yy = a*xx + b
                plt.plot(xx, yy, '--', color='black', linewidth=3, label='%s = %.4f*%s + %.4f\nR2 = %.2f' % (Yname, a, Xname, b, R2))
            plt.plot(x, y, 'ro', ms=7.5)
            plt.legend(loc='upper right')
            filename = self.main_output + '/%s-%s.pdf' % (Yname, Xname)
            plt.savefig(filename)
            plt.close()
    
    def build_histograms(self, data):
        for key, values in data.items():
            plt.grid(True)
            plt.xlabel(key)
            plt.yticks([])
            n, bins, patches = plt.hist(values, 15, normed=1, facecolor='green', alpha=0.75)
            filename = self.main_output + '/%s.pdf' % (key)
            plt.savefig(filename)
            plt.close()
    
    def stats(self, data, generations, times):
        self.statsfile = open('%s/stats' % (self.main_output), 'w')
        self.stats_convergence(data, generations, times)
        self.stats_variables(data)
        self.statsfile.close()

    def write_log(self, elite, generation, deviations, averages, time):
        # elite is the first pareto front
        # report best solution(s) at the current generation
        for individ in elite:
            reportstr = '%i ' % (generation)
            # report objective values
            for obj_name in self.objectives:
                value = individ.objectives[obj_name]
                reportstr += '%.16f ' % (value)
            # report variables values
            for var_name in self.var_ranges:
                value = individ.chromosome[var_name]
                reportstr += '%.16f ' % (value)
            reportstr += '\n'
            self.conv_log.write(reportstr)
        # report stats at the current generation
        reportstr = '%i ' % (generation)
        for objective in self.objectives:
            reportstr += '%.8f ' % (averages[objective])
            reportstr += '%.8f ' % (deviations[objective])
        for var_name in self.var_ranges:
            reportstr += '%.4f ' % (averages[var_name])
            reportstr += '%.4f ' % (deviations[var_name])
        reportstr += '%.1f\n' % (time)
        self.stats_log.write(reportstr)

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
            for var_name in self.var_ranges:
                value = data[var_name][0]
                s = '%s: %.4f\n' % (var_name, value)
                self.statsfile.write(s)
        if self.num_objectives > 1:
            s = 'PARETO FRONT: %i solutions\n' % (self.num_solutions)
            self.statsfile.write(s)
            for i in range(self.num_solutions):
                for objective in self.objectives:
                    s = '%s: %.8f\n' % (objective, data[objective][i])
                    self.statsfile.write(s)
                for var_name in self.var_ranges:
                    s = '%s: %.4f\n' % (var_name, data[var_name][i])
                    self.statsfile.write(s)
                s = '--------------------\n'
                self.statsfile.write(s)

        for objective in self.objectives:
            s = '\n%s\n' % (objective)
            self.statsfile.write(s)
            scores = data[objective]
            s = 'lowest: %.8f highest: %.8f average: %.8f median: %.8f std: %.8f\n' % (numpy.amin(scores), numpy.amax(scores), numpy.average(scores), numpy.median(scores), numpy.std(scores))
            self.statsfile.write(s)
        
        s = '\nGENERATIONS\n'
        self.statsfile.write(s)
        s = 'lowest: %i highest: %i average: %.1f median: %.1f std: %.1f\n\n' % (numpy.amin(generations), numpy.amax(generations), numpy.average(generations), numpy.median(generations), numpy.std(generations))
        self.statsfile.write(s)
        
        s = '\nTIMES\n'
        self.statsfile.write(s)
        s = 'lowest: %.3f highest: %.3f average: %.3f median: %.3f std: %.3f\n\n' % (numpy.amin(times), numpy.amax(times), numpy.average(times), numpy.median(times), numpy.std(times))
        self.statsfile.write(s)

    def stats_variables(self, data):
        s = 'VARIABLES\n'
        self.statsfile.write(s)
        for var_name in self.var_ranges:
            s = 'variable name: %s\n' % (var_name)
            self.statsfile.write(s)
            s = 'lowest: %.4f highest: %.4f average: %.4f median: %.4f std: %.4f\n\n' % (numpy.amin(data[var_name]), numpy.amax(data[var_name]), numpy.average(data[var_name]), numpy.median(data[var_name]), numpy.std(data[var_name]))
            self.statsfile.write(s)
    
    def dump_info(self, maxgen, size, crossrate, mutrate):
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
        for var_name in self.var_ranges:
            data[var_name] = [individ.chromosome[var_name] for individ in best_individuals]
        for obj_name in self.objectives:
            data[obj_name] = [individ.objectives[obj_name] for individ in best_individuals]
        return data
        
    def save_data(self, data):
        file = open('%s/solutions.csv' % (self.raw_output), 'wb') 
        writer = csv.writer(file, delimiter=' ', quoting=csv.QUOTE_NONE,quotechar='')
        for key, value in data.items():
            writer.writerow([key])
            writer.writerow(value)
        file.close()
    
    def save_details(self):
        file = open('%s/details.csv' % (self.raw_output), 'wb') 
        writer = csv.writer(file, delimiter=' ', quoting=csv.QUOTE_NONE, quotechar='')
        for key, value in self.var_ranges.items():
            writer.writerow([key])
            writer.writerow(value)
        file.close()
    
    def read_data(self,type):
        reader = csv.reader(open('%s.csv' % (type), 'rb'))
        i = 0
        data = {}
        for line in reader:
            value = line[0]
            if not i%2: 
                name = value
            else: 
                data[name] = [float(v) for v in value.split()]
            i+=1
        return data

    def open_logfiles(self, i):
        output_dir = '%s/%i' % (self.main_output, i)
        os.system('mkdir %s' % (output_dir) )
        self.conv_log = open('%s/convergence.log' % (output_dir),'w')
        self.stats_log = open('%s/statistics.log' % (output_dir),'w')
        self.write_header() # line with titles in outfile

    def close_logfiles(self):
        self.conv_log.close()
        self.stats_log.close()
