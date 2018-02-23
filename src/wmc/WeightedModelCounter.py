class WeightedModelCounter:
    """ Abstract class for weighted model counters. """

    def evaluate_cnf(self, cnf):
        """ Executes weighted model counting on a given weighted CNF. """
        raise NotImplementedError
