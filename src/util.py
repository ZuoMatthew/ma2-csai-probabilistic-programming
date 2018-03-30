import os.path
import problog_conversions.bn2problog
from problog.formula import LogicFormula
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF
from InferenceEngine import InferenceEngine

separator_1 = "===================================================="
separator_2 = "----------------------------------------------------"


def file_to_string(filename):
    with open(filename) as input_file:
        return input_file.read()


def load_problog_or_network_as_ground_problog(filename, is_network):
    if not is_network:
        program = file_to_string(filename)
        return ground_problog_program(program)
    else:
        ground_problog = problog_conversions.bn2problog.main(filename)

        ground_problog_no_comments = ""
        for line in ground_problog.splitlines():
            if len(line) and line[0] != "%":
                ground_problog_no_comments += line + os.linesep

        return ground_problog_no_comments


def ground_problog_program(program):
    """ Grounds a Problog program using the problog library. """
    lf = LogicFormula.create_from(program, avoid_name_clash=True, keep_order=True, label_all=True)
    return lf.to_prolog()


def evaluate_using_problog(program, print_steps=False):
    """ Evaluates a problog program using the problog library. """

    formula = LogicFormula.create_from(program, avoid_name_clash=True, keep_order=True, label_all=True)
    if print_steps:
        print("GROUND PROGRAM:")
        print(formula.to_prolog())
        print(separator_1)

    cnf = CNF.create_from(formula)  # type: CNF
    if print_steps:
        print("DIMACS:")
        print(cnf.to_dimacs(weighted=True, names=True))
        print(separator_1)

    ddnnf = DDNNF.create_from(cnf)
    results = ddnnf.evaluate()
    results = sorted(results.items(), key=lambda kv: str(kv[0]))
    results = [(str(q), p) for q, p in results]
    if print_steps:
        print("EVALUATION:")
        query_str_len = max([len(q) for q, _ in results])
        for query, probability in results:
            print("{:<{}}: {}".format(query, query_str_len, probability))

    return results


def results_with_pipeline(ground_program, counter="minic2d", print_steps=False):
    engine = InferenceEngine(counter)
    return engine.evaluate_ground_problog_program(ground_program, print_steps=print_steps)


def results_with_problog(ground_program, print_steps=False):
    return evaluate_using_problog(ground_program, print_steps)