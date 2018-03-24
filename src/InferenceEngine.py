import problog.formula
from CNF import CNF
from FOLTheory import FOLTheory
from ground_problog.GroundProblogParser import GroundProblogParser
from wmc.factory import create as create_weighted_model_counter


class InferenceEngine:
    def __init__(self):
        self.problog_parser = GroundProblogParser()
        self.weighted_model_counter = create_weighted_model_counter("SDD")

    def evaluate_problog_program(self, program):
        """ Evaluates a problog program.
        :type program: string
        """
        # ground and parse the program
        ground_program = self.ground_problog_program(program)
        problog_program = self.problog_parser.program_to_problog(ground_program)
        print("PROGRAM")
        print(problog_program)
        print("====================================================")

        # convert the GroundProblog to a FOLTheory
        fol_theory = FOLTheory.create_from_problog(problog_program)
        print("FOL theory:")
        print(fol_theory)
        print("====================================================")

        # convert the LogicFormula to its CNF representation
        cnf = CNF.create_from_fol_theory(fol_theory)
        print("CNF:")
        print(cnf)
        print("====================================================")

        # convert the CNF to dimacs format for the weighted model counter
        print("DIMACS")
        print(cnf.to_minic2d() + "====================================================")

        # do the model counting
        results = self.weighted_model_counter.evaluate_cnf(cnf)
        print("RESULT:")
        for query, probability in results:
            print("Query:", query)
            print("Probability:", probability)
            print()

        return results

    def evaluate_bayesian_network(self, network):
        """ Evaluates a Bayesian network by converting it to a Problog program and evaluating that program. """
        # return self.evaluate_problog_program(program)
        raise NotImplementedError

    def ground_problog_program(self, program):
        """ Grounds a Problog program using the Problog library. """
        lf = problog.formula.LogicFormula.create_from(program, avoid_name_clash=True, keep_order=True, label_all=True)
        return lf.to_prolog()
