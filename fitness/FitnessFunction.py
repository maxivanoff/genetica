
class FitnessFunction(object):
    """
    Abstract class. 

    set_scores updates individuals' scores
    """
    
    def set_scores(self, individual):
        """
        actual fitness function
        sets score for each objective
        """
        for objective in individual.objectives:
            score = None # calculation of the score goes here
            invidividual.objectives[objective] = score

class Parallel(FitnessFunction):

    def __init__(self, fitness, comm, total_jobs):
        self.set_scores = fitness
        self.comm = comm
        self.rank = self.comm.Get_rank() # number of current processor
        self.num_proc = self.comm.Get_size() # number of processors
        num_proc_jobs = total_jobs/float(self.num_proc) # number of tasks per proc; must be integer
        self.num_proc_jobs = int(num_proc_jobs)
        if self.num_proc_jobs!=num_proc_jobs:
            print 'Tasks per processor: %.1f\nNumber of tasks: %i\nNumber of processors: %i' % (num_proc_jobs, total_jobs, self.num_proc)
            raise NameError('Number of tasks per processor must be integer')
    
    def calculation(self, individuals):
        """
        Environment calls this method to perform fitness function calculation
        """
        self.more_work()
        self.masters_work(individuals)
    
    def more_work(self):
        for proc in range(self.num_proc):
            self.comm.send(False, dest=proc, tag=proc) # say to all proc that work is not done
    
    def close(self):
        """
        Environment calls this method at the end of the algorithm to stop the waiting of slaves. 
        see slaves_work()
        """
        for proc in range(self.num_proc):
            self.comm.send(True, dest=proc, tag=proc) # say to all proc that work is done

    def masters_work(self, individuals):
        self.send_data(individuals) # master sends data to slaves
        self.calculate(individuals[:self.num_proc_jobs]) # first individuals are calculated by master
        self.recieve_results(individuals)

    def send_data(self, individuals):
        for proc in range(1, self.num_proc):
            offset = proc*self.num_proc_jobs
            data2send = individuals[offset:offset + self.num_proc_jobs]
            self.comm.send(data2send, dest=proc,tag=proc)

    def recieve_results(self, individuals):
        for proc in range(1, self.num_proc):
            offset = proc*self.num_proc_jobs
            rcvd_results = self.comm.recv(source=proc, tag=proc)
            individuals[offset:offset + self.num_proc_jobs] = rcvd_results[:]
    
    def calculate(self, individuals):
        for individual in individuals:
            self.set_scores(individual)

    def slaves_work(self):
        while not self.work_done():
            rcvd_data = self.comm.recv(source=0, tag=self.rank)
            self.calculate(rcvd_data)
            self.comm.send(rcvd_data, dest=0, tag=self.rank)
    
    def work_done(self): # slaves wait to know if work is done
        return self.comm.recv(source=0, tag=self.rank)

class Single(FitnessFunction):

    def __init__(self, fitness):
        self.set_scores = fitness

    def calculation(self, individuals):
        for individual in individuals:
            self.set_scores(individual)

    def close(self):
        """
        Environment calls this method at the end of the algorithm.
        """
        pass

    

