import copy
import util
import os.path
from timeit import default_timer as timer


class WeightedModelCounter:
    """ Abstract class for weighted model counters. """

    def evaluate_cnf(self, cnf, print_steps=False):
        """ Executes queries in a given weighted CNF and returns the results. """
        start = timer()
        results = {}
        stats = {}

        cnf_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "files", "cnf{}.dimac"))
        cnf_query_filename = cnf_filename.format("")
        cnf_no_query_filename = cnf_filename.format("_no_query")

        evidence = cnf.get_evidence_with_dimacs_numbers()
        queries = cnf.get_queries_with_dimacs_numbers()

        query_stats = {}
        for literal, number in queries:
            query_start = timer()
            cnf_with_query = copy.deepcopy(cnf)
            cnf_with_query.add_clause([literal])
            if print_steps:
                print("EVALUATING QUERY '{}', DIMACS NUMBER {}".format(literal, number))

            with open(cnf_query_filename, "w") as file:
                file.write(cnf_with_query.to_dimacs())

            # do model count of (theory + evidence + query)
            probability, memory_usage = self.do_model_count(cnf_query_filename)
            if print_steps:
                print("RESULT: {}".format(probability))

            # if CNF has evidence, then need to divide probability by model count of (theory + evidence)
            if len(evidence):
                with open(cnf_no_query_filename, "w") as file:
                    file.write(cnf.to_dimacs())

                # do model count of (theory + evidence)
                probability_no_query, memory_usage = self.do_model_count(cnf_no_query_filename)
                if print_steps:
                    print("RESULT WITHOUT QUERY: {}".format(probability_no_query))

                probability = probability / probability_no_query

            results[str(literal)] = probability

            if print_steps and literal != queries[-1][0]:
                print(util.separator_2)
            query_stats[str(literal)] = timer() - query_start

        stats["duration of cnf evaluation of queries"] = query_stats
        stats["duration of cnf evaluation"] = timer() - start

        return sorted(results.items(), key=lambda kv: kv[0]), stats

    def do_model_count(self, cnf):
        """ Executes weighted model counting on a given weighted CNF and returns it's probability. """
        raise NotImplementedError
