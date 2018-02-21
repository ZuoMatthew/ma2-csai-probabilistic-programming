import util
from CNF2 import CNF
from FOLTheory import FOLTheory
from GroundProblogParser import GroundProblogParser


def parse_to_CNF(filename):
    """ Converts a ground problog program to its CNF representation. """
    program = util.file_to_string(filename)

    # parse the program
    parser = GroundProblogParser()
    problog = parser.program_to_problog(program)
    print("PROGRAM")
    print(problog)
    print("====================================================")

    # convert the GroundProblog to a FOLTheory
    fol_theory = FOLTheory.create_from_problog(problog)
    print("FOL theory:")
    print(fol_theory)
    print("====================================================")

    # convert the LogicFormula to its CNF representation
    cnf = CNF.create_from_fol_theory(fol_theory)
    print("CNF:")
    print(cnf)
    print("====================================================")
    print("DIMACS")
    print(cnf.to_dimacs() + "====================================================")
    return cnf


if __name__ == '__main__':
    cnf = parse_to_CNF("../files/test.grounded.pl")
