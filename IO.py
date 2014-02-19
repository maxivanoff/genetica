import os
import numpy

class Output(object):

    def __init__(self, problem_name, var_ranges, maxgenerations, size, crossrate, mutrate):
        self.problem_name = problem_name
        self.var_ranges = var_ranges ## dictionary, it has names of variables
        if not os.path.exists('./output'):
            os.system('mkdir ./output')
        self.MainOutputDir = './output/%s' % (self.problem_name)
        if os.path.exists(self.MainOutputDir):
            os.system('rm -r %s' % (self.MainOutputDir))
            os.system('mkdir %s' % (self.MainOutputDir))
        else:
            os.system('mkdir %s' % (self.MainOutputDir))
        self.dump_info(maxgenerations, size, crossrate, mutrate)

    def dump_info(self, maxgen, size, crossrate, mutrate):
        infofile = open('%s/info' % (self.MainOutputDir), 'w')
        s = 'Maximum generations: %i\n' % (maxgen)
        infofile.write(s)
        s = 'Population size: %i\n' % (size)
        infofile.write(s)
        s = 'Crossover rate: %.3f\n' % (crossrate)
        infofile.write(s)
        s = 'Mutation rate: %.3f\n' % (mutrate)
        infofile.write(s)
        infofile.close()

    
    def open_logfiles(self, i):
        self.statsfile = open('%s/stats' % (self.MainOutputDir), 'w')
        self.OutputDirName = '%s/%i' % (self.MainOutputDir, i)
        os.system('mkdir %s' % (self.OutputDirName) )
        self.conv_log = open('%s/convergence.log' % (self.OutputDirName,),'w')
        self.stats_log = open('%s/statistics.log' % (self.OutputDirName,),'w')
        self.write_header() # line with titles in outfile

    def write_log(self, elite, generation, deviations, averages, time):
        # elite is the first pareto front
        prms = ''
        # report best solution(s) at the current generation
        for individ in elite:
            reportstr = '%i ' % (generation)
            # report objective values
            for objective in individ.objectives:
                reportstr += '%.8f ' % (objective)
            # report variables values
            for var_name in self.var_ranges:
                value = individ.chromosome[var_name]
                reportstr += '%.4f ' % (value)
            reportstr += '\n'
        self.cov_log.write(reportstr)
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
        reportstr = 'gen best_score  '
        prms = ''
        for var_name in self.var_ranges:
            prms += 'best_%s ' % (var_name)
        reportstr += prms + 'ave_score '
        prms = ''
        for var_name in self.var_ranges:
            prms += 'ave_%s  ' % (var_name)
        reportstr += prms + 'dev_score '
        prms = ''
        for var_name in self.var_ranges:
            prms += 'dev_%s  ' % (var_name)
        reportstr += prms + 'time\n'
        self.outfile.write(reportstr)
    
    def write_final(self, best_individuals, generations, times):
        self.stats(best_individuals, generations, times)
        self.final_graphical_data(best_individuals)
    
    def stats_convergence(self, best_individuals, generations, times):
        best_individuals.sort()
        s = 'BEST SOLUTION\n'
        self.statsfile.write(s)
        for var_name in self.var_ranges:
            value = best_individuals[0].chromosome[var_name]
            s = '%s: %.4f\n' % (var_name, value)
            self.statsfile.write(s)
        scores = []
        for individ in best_individuals:
            scores.append(individ.score)
        s = '\nSCORES\n'
        self.statsfile.write(s)
        s = 'lowest: %.8f highest: %.8f average: %.8f median: %.8f std: %.8f\n\n' % (numpy.amin(scores), numpy.amax(scores), numpy.average(scores), numpy.median(scores), numpy.std(scores))
        self.statsfile.write(s)
        
        s = 'GENERATIONS\n'
        self.statsfile.write(s)
        s = 'lowest: %i highest: %i average: %.1f median: %.1f std: %.1f\n\n' % (numpy.amin(generations), numpy.amax(generations), numpy.average(generations), numpy.median(generations), numpy.std(generations))
        self.statsfile.write(s)
        
        s = '\nTIMES\n'
        self.statsfile.write(s)
        s = 'lowest: %.3f highest: %.3f average: %.3f median: %.3f std: %.3f\n\n' % (numpy.amin(times), numpy.amax(times), numpy.average(times), numpy.median(times), numpy.std(times))
        self.statsfile.write(s)

    def stats_variables(self, chromosomes):
        s = 'VARIABLES\n'
        self.statsfile.write(s)
        prms = {}
        for var_name in chromosomes[0]:
            prms[var_name] = []
            for chromosome in chromosomes:
                prms[var_name].append(chromosome[var_name])

        for var_name in chromosomes[0]:
            s = 'variable name: %s\n' % (var_name)
            self.statsfile.write(s)
            s = 'lowest: %.4f highest: %.4f average: %.4f median: %.4f std: %.4f\n\n' % (numpy.amin(prms[var_name]), numpy.amax(prms[var_name]), numpy.average(prms[var_name]), numpy.median(prms[var_name]), numpy.std(prms[var_name]))
            self.statsfile.write(s)

    def close_logfiles(self):
        self.outfile.close()
