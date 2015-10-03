import itertools
import matplotlib.pyplot as plt
import numpy as np
delta = 0.5
s = 8.
a = 0.05
v = 0.7

class Output(object):

    def __init__(self, name, ranges, objectives, settings):
        self.name = name
        self.ranges = ranges
        self.objectives = objectives
        self.generations = settings['maximum generations']
        self.size = settings['size']
        X = np.arange(-4, 12, 0.25)
        Y = np.arange(-6, 6, 0.25)

        X, Y = np.meshgrid(X, Y)
        R = (a*(X-s)**2 + delta - a*X*X)**2 + 4*v*v
        self.Z = (a*(X-s)**2 + delta + a*X*X - np.sqrt(R))*0.5 - 0.5*(a*s*s + delta - np.sqrt((a*s*s + delta)**2 + 4*v*v)) + 0.05*Y*Y
        self.X =X
        self.Y = Y
        for i in xrange(self.generations):
            data = self.read_log(i)
            self.correlate_pairs(data,i)
            if i == 0:
                self.full_data = data.copy()
            else:
                self.merge_data(data)

    def merge_data(self, data):



    def correlate_pairs(self, data, generation):
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
                Xname = pair[0]
                Yname = pair[1]
            x = data[Xname]
            y = data[Yname]
            if Xname in self.ranges: xlim = self.ranges[Xname]
            else: xlim = [min(x), max(x)]
            if Yname in self.ranges: ylim = self.ranges[Yname]
            else: ylim = [min(y), max(y)]
            plt.grid(True)
            plt.xlabel(Xname)
            plt.ylabel(Yname)
            plt.ylim(ylim)
            plt.xlim(xlim)
            levels = np.array([-0.1, 0.2, 0.57, 0.85, 1.5, 2.0, 2.5, 3.0, 3.5])
            plt.contourf(self.X, self.Y, self.Z, cmap=plt.cm.coolwarm, levels=levels)
            plt.contour(self.X, self.Y, self.Z,  colors='black',levels=levels)
            plt.plot(x, y, 'ro', ms=7.5)
            filename = './output/%s/%03i-%s-%s.pdf' % (self.name, generation, Yname, Xname)
            plt.savefig(filename)
            plt.close()

    def read_log(self, generation):
        file = open('./output/%s/%03i.log' % (self.name, generation), 'r')
        keys = file.readline().split()
        data = {}
        for key in keys:
            data[key] = []
        for _ in xrange(self.size):
            l = file.readline()
            values = map(lambda v: float(v), l.split())
            for key, value in zip(keys, values):
                data[key].append(value)
        return data

