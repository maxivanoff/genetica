class Results(object):
    """
    contains results of one GA cycle 
    """
    
    def __init__(self):
        self.best = []
        self.generations = []
        self.deviations = []
        self.averages = []
        self.times = []
        self.individuals = []

    def report(self, results):
        self.best.append(results['best'])
        self.generations.append(results['gen'])
        self.deviations.append(results['deviations'])
        self.averages.append(results['averages'])
        self.times.append(results['time'])
        self.individuals.append(results['individuals'])

    def __add__(self, results):
        new_results = self.__class__()


