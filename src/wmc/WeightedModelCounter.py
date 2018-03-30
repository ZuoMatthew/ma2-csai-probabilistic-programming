import copy
import util
import os.path


class WeightedModelCounter:
    """ Abstract class for weighted model counters. """

    def evaluate_cnf(self, cnf, print_steps=False):
        """ Executes queries in a given weighted CNF and returns the results. """
        print_steps = False
        results = {}

        cnf_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "files", "cnf{}.dimac"))
        cnf_query_filename = cnf_filename.format("")
        cnf_no_query_filename = cnf_filename.format("_no_query")

        evidence = cnf.get_evidence_with_dimacs_numbers()
        queries = cnf.get_queries_with_dimacs_numbers()

        for literal, number in queries:
            cnf_with_query = copy.deepcopy(cnf)
            cnf_with_query.add_clause([literal])
            if print_steps:
                print("DIMACS WITH QUERY:")
                print(cnf_with_query.to_dimacs())

            with open(cnf_query_filename, "w") as file:
                file.write(cnf_with_query.to_dimacs())

            probability, memory_usage = self.do_model_count(cnf_query_filename)

            if print_steps:
                print("RESULT: {}".format(probability))

            # model count just done is of (theory + evidence + query)
            # if CNF has evidence, then need to divide probability by modelcount of (theory + evidence)
            if len(evidence):
                with open(cnf_no_query_filename, "w") as file:
                    file.write(cnf.to_dimacs())
                probability_no_query, memory_usage = self.do_model_count(cnf_no_query_filename)
                if print_steps:
                    print("RESULT WITHOUT QUERY: {}".format(probability_no_query))
                probability = probability / probability_no_query

            results[str(literal)] = probability

            if print_steps and literal != queries[-1][0]:
                print(util.separator_2)

        if print_steps:
            print(util.separator_1)
        return sorted(results.items(), key=lambda kv: kv[0])

    def do_model_count(self, cnf):
        """ Executes weighted model counting on a given weighted CNF and returns it's probability. """
        raise NotImplementedError
