'''
module contains general form of fitness function and its MPI realization
'''

class MPIDistribution(object):

    def __init__(self, comm, NumTasks, function):
        self.comm = comm
        self.function = function
        self.rank = self.comm.Get_rank() # number of current processor
        self.num_proc = self.comm.Get_size() # number of processors
        TasksPerProc = NumTasks/float(self.num_proc) # number of tasks per proc; must be integer
        self.TasksPerProc = int(TasksPerProc)
        if self.TasksPerProc!=TasksPerProc:
            print 'Tasks per processor: %.1f\nNumber of tasks: %i\nNumber of processors: %i' % (self.TasksPerProc, NumTasks, self.num_proc)
            raise NameError('Number of tasks per processor must be integer')
    
    def calculation(self, data):
        """
        Environment calls this method to perform fitness function calculation
        data is a list of individuals
        """
        self.more_work()
        self.masters_work(data)
    
    def more_work(self):
        for proc in range(self.num_proc):
            self.comm.send(False, dest=proc, tag=proc) # say to all proc that work is not done
    
    def close(self):
        """
        Environment calls this method at the end of the algorithm to stop the waiting of slaves. see slaves_work()
        """
        for proc in range(self.num_proc):
            self.comm.send(True, dest=proc, tag=proc) # say to all proc that work is done

    def masters_work(self, data):
        self.send_data(data) # master sends data to slaves
        self.recieve_results(data)

    def send_data(self, data):
        pass

    def recieve_results(self, data):
        pass
    
    def calculate(self, data):
        results = []
        for unit in data:
            result = self.function(unit)
            results.append(result)
        return results

    def slaves_work(self):
        while not self.work_done():
            rcvd_data = self.comm.recv(source=0, tag=self.rank)
            results = self.calculate(rcvd_data)
            self.comm.send(results, dest=0, tag=self.rank)
    
    def work_done(self): # slaves wait to know if work is done
        return self.comm.recv(source=0, tag=self.rank)

class NoDistribution(object):

    def __init__(self, function):
        self.function = function
    
    def calculation(self, individuals):
        for individ in individuals:
            individ.objectives = self.function(individ.chromosome)

    def close(self):
        pass


class GeneralFitnessFunction(object):
    """
    Abstract class. 
    For parallel execution is combined with MPIDistribution class
    For one-processor execution is combined with NoDistribution class

    get_scores returns objectives scores for a given chromosome
    """
    
    def __init__(self, objectives):
        self.objectives = objectives

    def f(self, objective_name, chromosome):
        """
        actual fitness function
        returns a score of the chromosome for a given objective name
        """
        if objective_name == 'objective1':
            score = None
        if objective_name == 'objective2':
            score = None
        return score
    
    def get_scores(self, chromosome):
        scores = []
        for objective in self.objectives:
            scores.append(self.f(objective, chromosome))
        objectives = dict((o, s) for o, s in zip(self.objectives, scores))
        return objectives

class Single(NoDistribution, GeneralFitnessFunction):
    
    def __init__(self, objectives, f):
        GeneralFitnessFunction.__init__(self, objectives)
        NoDistribution.__init__(self, self.get_scores)
        self.f = f

   
class Parallel(MPIDistribution, GeneralFitnessFunction):

    def __init__(self, objectives, f, comm, size):
        GeneralFitnessFunction.__init__(self, objectives)
        MPIDistribution.__init__(self, comm, size, self.get_scores)
        self.f = f
    
    def send_data(self, individuals):
        for proc in range(self.num_proc):
            offset = proc*self.TasksPerProc
            data2send = [individ.chromosome for individ in individuals[offset:offset + self.TasksPerProc]]
            if proc==0:
                masters_data = data2send 
            else:
                self.comm.send(data2send, dest=proc,tag=proc)
        self.masters_results = self.calculate(masters_data)

    def recieve_results(self, individuals):
        for i in range(self.TasksPerProc):
            individuals[i].objectives = self.masters_results[i]
        for proc in range(1, self.num_proc):
            rcvd_results = self.comm.recv(source=proc, tag=proc)
            for i in range(self.TasksPerProc):
                individual = individuals[proc*self.TasksPerProc + i]
                individual.objectives = rcvd_results[i]

