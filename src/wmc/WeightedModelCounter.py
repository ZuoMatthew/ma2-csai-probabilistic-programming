import copy
import util


class WeightedModelCounter:
    """ Abstract class for weighted model counters. """

    def evaluate_cnf(self, cnf):
        """ Executes queries in a given weighted CNF and returns the results. """
        results = {}
        cnf_filename = "../files/test.cnf"

        queries = cnf.get_queries_with_dimacs_numbers()
        for literal, number in queries:
            cnf_with_query = copy.deepcopy(cnf)
            cnf_with_query.add_clause([literal])
            dimacs = cnf_with_query.to_dimacs()
            print("DIMACS WITH QUERY:")
            print(dimacs)
            if literal != queries[-1][0]:
                print(util.separator_2)

            with open(cnf_filename, "w") as file:
                file.write(dimacs)

            probability = self.do_model_count(cnf_filename)
            results[str(literal)] = probability

        print(util.separator_1)
        return sorted(results.items(), key=lambda kv: kv[0])

    def do_model_count(self, cnf):
        """ Executes weighted model counting on a given weighted CNF and returns it's probability. """
        raise NotImplementedError
