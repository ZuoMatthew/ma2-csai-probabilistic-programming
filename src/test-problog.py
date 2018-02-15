from problog.program import PrologString
from problog.formula import LogicFormula, LogicDAG
from problog.logic import Term
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF

with open("files/monty_hall.pl") as input_file:
        input_code = input_file.read()

p = PrologString(input_code)
lf = LogicFormula.create_from(p)
dag = LogicDAG.create_from(lf)
cnf = CNF.create_from(dag)
print(cnf.to_dimacs())
ddnnf = DDNNF.create_from(cnf)    # compile CNF to ddnnf
ddnnf.evaluate()