import copy

import util as util
from timeit import default_timer as timer
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
        start = timer()
        ttime = timer()
        # parse the ground program to the internal representation of ground problog
        problog_program = self.problog_parser.program_to_problog(ground_program)
        if print_steps:
            print("GROUND PROGRAM:")
            print(problog_program)
            print(util.separator_1)
        time_parsed_ground_problog = str(round(timer() - ttime, 3)) + "s"
        ttime = timer()

        # convert the GroundProblog to a FOLTheory
        fol_theory = FOLTheory.create_from_problog(problog_program)
        if print_steps:
            print("FOL theory:")
            print(fol_theory)
            print(util.separator_2)
        time_converted_to_fol = str(round(timer() - ttime, 3)) + "s"
        ttime = timer()

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
        time_converted_to_cnf = str(round(timer() - ttime, 3)) + "s"
        ttime = timer()

        # do the model counting
        results, stats = self.weighted_model_counter.evaluate_cnf(cnf, print_steps)
        time_model_counting = str(round(timer() - ttime, 3)) + "s"
        time_total = str(round(timer() - start, 3)) + "s"

        stats["Time to parse ground problog"] = time_parsed_ground_problog
        stats["Time to convert ground problog to first order logic"] = time_converted_to_fol
        stats["Time to convert first order logic to CNF"] = time_converted_to_cnf
        stats["Time for all model counting"] = time_model_counting
        stats["Total runtime"] = time_total
        if print_steps:
            print(util.separator_1)
            print("EVALUATION:")
            query_str_len = max([len(q) for q, _ in results]) if results else None
            for query, probability in results:
                print("{:<{}}: {}".format(query, query_str_len, probability))

            print(util.separator_2)
            print("STATS:")
            for stat in stats:
                print("\t" + stat + ": ", stats[stat])

        return results

    def interpretation_to_cnf_evidence(self, interpretation):
        """ Converts a ProbLog interpretation to a list of CNF evidence. """
        problog_program = self.problog_parser.program_to_problog(interpretation)
        fol_theory = FOLTheory.create_from_problog(problog_program)
        cnf = CNF.create_from_fol_theory(fol_theory)
        return cnf.get_evidence()

    def ground_problog_learn_parameters(self, ground_program, interpretations, print_steps=False):
        """ Learns parameters in a ground_problog file using Expectation Maximization. """
        start = timer()

        # initial values for the probabilities to be learned have already been set during parsing

        # parse the ground program to the internal representation of ground problog
        problog_program = self.problog_parser.program_to_problog(ground_program)
        if print_steps:
            print("GROUND PROGRAM:")
            print(problog_program)
            print(util.separator_1)

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

        # get the probabilities that need to be learned/tuned
        tunable_probabilities = problog_program.get_tunable_probabilities_as_dict()
        if print_steps:
            print("INITIAL TUNABLE PROBABILITIES:")
            print(tunable_probabilities)
            print(util.separator_1)
        iteration = 0
        converged = False

        while not converged and iteration < 100:
            iteration += 1

            # update the weights of the tunable probabilities in the CNF at every iteration
            for tunable_prob_name in tunable_probabilities:
                prob = tunable_probabilities[tunable_prob_name]
                cnf.set_literal_weights(tunable_prob_name, prob, 1 - prob)

            # add each interpretation as evidence to the CNF and sum up the results of the queries
            probability_sums = dict.fromkeys(tunable_probabilities.keys(), 0)
            for interpretation in interpretations:
                # add the interpretation as evidence in a copy of the CNF
                cnf_copy = copy.deepcopy(cnf)
                for evidence in self.interpretation_to_cnf_evidence(interpretation):
                    cnf_copy.add_evidence(evidence)

                # do model counting with the evidence
                results, _ = self.weighted_model_counter.evaluate_cnf(cnf_copy, print_steps=False)
                for query, probability in results:
                    probability_sums[query] += probability

            # update the tunable probabilities and determine whether or not convergence has been reached
            all_converged = True
            for probability in probability_sums:
                new_probability = probability_sums[probability] / len(interpretations)

                if abs(tunable_probabilities[probability] - new_probability) > 0.005:
                    all_converged = False

                tunable_probabilities[probability] = new_probability

            converged = all_converged
            print("probabilities after iteration {}: {}".format(iteration, tunable_probabilities))

        if print_steps:
            print(util.separator_1)
            print("FINAL LEARNED PARAMETERS:")
            query_str_len = max([len(k) for k in tunable_probabilities.keys()])
            for query, probability in tunable_probabilities.items():
                print("{:<{}}: {}".format(query, query_str_len, probability))

        print("Total runtime:", str(round(timer() - start, 3)) + "s")
        return tunable_probabilities
