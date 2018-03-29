import util as util
from CNF import CNF
from FOLTheory import FOLTheory
from ground_problog.GroundProblogParser import GroundProblogParser
from wmc.factory import create as create_weighted_model_counter


class InferenceEngine:
    def __init__(self, counter="sdd"):
        self.problog_parser = GroundProblogParser()
        self.weighted_model_counter = create_weighted_model_counter(counter)

    def evaluate_problog_program(self, program, print_steps=False):
        """ Evaluates a problog program and returns the results. """
        # ground and parse the program
        ground_program = util.ground_problog_program(program)

        problog_program = self.problog_parser.program_to_problog(ground_program)
        if print_steps:
            print("GROUND PROGRAM")
            print(problog_program)
            print(util.separator_1)

        problog_program = problog_program.preprocess_ground()
        # convert the GroundProblog to a FOLTheory
        fol_theory = FOLTheory.create_from_problog(problog_program)
        if print_steps:
            print("FOL theory:")
            print(fol_theory)
            print(util.separator_2)

            print("FOL theory in CNF:")
            print(fol_theory.to_cnf().formulas[0])
            print(util.separator_1)

        # convert the LogicFormula to its CNF representation
        cnf = CNF.create_from_fol_theory(fol_theory)
        if print_steps:
            print("CNF:")
            print(cnf)
            print(util.separator_1)

            # convert the CNF to dimacs format for the weighted model counter
            print("DIMACS")
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

    def evaluate_bayesian_network(self, network):
        """ Evaluates a Bayesian network by converting it to a Problog program and evaluating that program. """
        # https://github.com/jordn/ProbLog/blob/master/conversions/bn2problog.py
        # return self.evaluate_problog_program(program)
        raise NotImplementedError
