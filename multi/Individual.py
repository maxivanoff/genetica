from genetica.common import Individual

class RDGAIndividual(Individual.RealCoded):
    def __init__(self, gene_ranges):
        Individual.RealCoded.__init__(self, gene_ranges)
        self.rank = None
        self.density = None
        self.coordinates = {} # in objective space

    def get_rd(self):
        return (self.rank, self.density)
