from Output import Output 


class Out(Output):
    def __init__(self):
        self.var_ranges = self.read_data('details')       
        self.data = self.read_data('solutions')
        self.main_output = '.'

O = Out()
O.correlate_pairs(O.data)
O.build_histograms(O.data)
