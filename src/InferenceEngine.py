import copy

import util as util
from CNF import CNF
from FOLTheory import FOLTheory
from ground_problog.GroundProblogParser import GroundProblogParser
from wmc.factory import create as create_weighted_model_counter


class InferenceEngine:
    def __init__(self, counter="minic2d"):
        self.problog_parser = GroundProblogParser()
        self.weighted_model_counter = create_weighted_model_counter(counter)

    def ground_problog_evaluate(self, ground_program, print_steps=False):
        """ Evaluates a problog program and returns the results. """
        # parse the ground program to the internal representation of ground problog
        problog_program = self.problog_parser.program_to_problog(ground_program)
        if print_steps:
            print("GROUND PROGRAM")
            print(problog_program)
            print(util.separator_1)

        # convert the GroundProblog to a FOLTheory
        fol_theory = FOLTheory.create_from_problog(problog_program)
        if print_steps:
            print("FOL theory:")
            print(fol_theory)
            print(util.separator_2)

        # convert the FOLTheory to its CNF representation
        cnf = CNF.create_from_fol_theory(fol_theory)
        if print_steps:
            print("CNF:")
            print(cnf)
            print(util.separator_1)

            # convert the CNF to dimacs format for the weighted model counter
            print("DIMACS:")
            print(cnf.to_dimacs())
            print(util.separator_1)

        # do the model counting
        results = self.weighted_model_counter.evaluate_cnf(cnf, print_steps)
        if print_steps:
            print("EVALUATION:")
            query_str_len = max([len(q) for q, _ in results]) if results else None
            for query, probability in results:
                print("{:<{}}: {}".format(query, query_str_len, probability))

        return results

    def interpretation_to_cnf_evidence(self, interpretation):
        """ Converts a ProbLog interpretation to a list of CNF evidence. """
        problog_program = self.problog_parser.program_to_problog(interpretation)
        fol_theory = FOLTheory.create_from_problog(problog_program)
        cnf = CNF.create_from_fol_theory(fol_theory)
        return cnf.get_evidence()

    def ground_problog_learn_parameters(self, ground_program, interpretations, print_steps=False):
        """ Learns parameters in a ground_problog file using Expectation Maximization. """
        # parse the ground program to the internal representation of ground problog
        problog_program = self.problog_parser.program_to_problog(ground_program)
        if print_steps:
            print("GROUND PROGRAM")
            print(problog_program)
            print(util.separator_1)

        # get the probabilities that need to be learned/tuned
        tunable_probabilities = problog_program.get_tunable_probabilities_as_dict()
        if print_steps:
            print("INITIAL TUNABLE PROBABILITIES")
            print(tunable_probabilities)

        # convert the GroundProblog to a FOLTheory
        fol_theory = FOLTheory.create_from_problog(problog_program)
        # add the probabilities to be learned as queries in the FOLTheory
        fol_theory.delete_queries()
        for term in problog_program.get_tunable_probabilities():
            fol_theory.add_query_from_problog_term(term)

        if print_steps:
            print("FOL theory:")
            print(fol_theory)
            print(util.separator_2)

        # convert the FOLTheory to its CNF representation
        cnf = CNF.create_from_fol_theory(fol_theory)
        if print_steps:
            print("CNF:")
            print(cnf)
            print(util.separator_1)

            # convert the CNF to dimacs format for the weighted model counter
            print("DIMACS:")
            print(cnf.to_dimacs())
            print(util.separator_1)

        convergence = False
        iteration = 1
        while not convergence:
            for tp in tunable_probabilities:
                # TODO: set the weights of the tunable_probabilities every iteration
                p = tunable_probabilities[tp]
                cnf.set_weights(tp, p, 1 - p)

            sums = dict.fromkeys(tunable_probabilities.keys(), 0)
            M = 0
            for interpretation in interpretations:
                M += 1
                cnf_copy = copy.deepcopy(cnf)
                # add the interpretation as evidence in the CNF
                for evidence in self.interpretation_to_cnf_evidence(interpretation):
                    cnf_copy.add_evidence(evidence)

                # Do model counting with the evidence
                results = self.weighted_model_counter.evaluate_cnf(cnf_copy, print_steps)
                for query, probability in results:
                    # TODO: add the results (DONE?)
                    sums[query] += probability

            # TODO: update the probabilities (DONE?)
            for probability in sums:
                tunable_probabilities[probability] = sums[probability] / M

            print("probabilities after iteration {}: {}".format(iteration, tunable_probabilities))

        if print_steps:
            print("FINAL LEARNED PARAMETERS:")
            query_str_len = max([len(k) for k in tunable_probabilities.keys])
            for query, probability in tunable_probabilities.items():
                print("{:<{}}: {}".format(query, query_str_len, probability))

        return tunable_probabilities
