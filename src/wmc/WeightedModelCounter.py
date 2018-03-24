class WeightedModelCounter:
    """ Abstract class for weighted model counters. """

    def evaluate_cnf(self, cnf):
        """ Executes queries in a given weighted CNF and returns the results. """
        results = []
        dimacs = cnf.to_dimacs()
        queries = cnf.get_queries_with_dimacs_numbers()

        for literal, number in queries:
            cnf_with_query = dimacs + "1.0 {}{} 0\n".format("-" if literal.negated else "", number)
            probability = self.do_model_count(cnf_with_query)
            print("DOING QUERY:")
            print(cnf_with_query, "----------------------------------------------------")
            results.append((str(literal), probability))

        return results

    def do_model_count(self, cnf):
        """ Executes weighted model counting on a given weighted CNF and returns it's probability. """
        raise NotImplementedError
