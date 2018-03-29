import os.path
from problog.formula import LogicFormula
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF
from InferenceEngine import InferenceEngine

separator_1 = "===================================================="
separator_2 = "----------------------------------------------------"


def file_to_string(filename):
    with open(filename) as input_file:
        return input_file.read()


def load_problog_program(filename):
    filename = os.path.join(os.path.dirname(__file__), "files", "problog", filename)
    return file_to_string(filename)


def ground_problog_program(program):
    """ Grounds a Problog program using the problog library. """
    lf = LogicFormula.create_from(program, avoid_name_clash=True, keep_order=True, label_all=True)
    return lf.to_prolog()


def evaluate_using_problog(program, print_steps=False):
    """ Evaluates a problog program using the problog library. """
    formula = LogicFormula.create_from(program, avoid_name_clash=True, label_all=True)
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


def results_with_pipeline(filename, print_steps=False):
    program = load_problog_program(filename)
    engine = InferenceEngine()
    return engine.evaluate_problog_program(program, print_steps)


def results_with_problog(filename, print_steps):
    program = load_problog_program(filename)
    return evaluate_using_problog(program, print_steps)
