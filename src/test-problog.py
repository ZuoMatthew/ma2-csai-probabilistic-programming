from problog.program import PrologString
from problog.formula import LogicFormula, LogicDAG
from problog.logic import Term
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF

with open("files/monty_hall.pl") as input_file:
        input_code = input_file.read()

program = PrologString("""0.3::a.  query(a).""")

formula = LogicFormula.create_from(program)
print("PROLOG:\n", formula.to_prolog(), "\n")

cnf = CNF.create_from(formula)
print("CNF:\n", cnf.to_dimacs())

ddnnf = DDNNF.create_from(cnf)
print("EVALUATION:\n", ddnnf.evaluate())