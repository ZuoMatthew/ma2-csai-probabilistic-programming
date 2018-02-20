from problog.program import PrologString
from problog.formula import LogicFormula, LogicDAG
from problog.logic import Term
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF
import util

program = util.file_to_string("../files/test.grounded.pl")
# program = PrologString("""
# 0.3::a.
# 0.6::b.
# 0.1::c :- a.
# c :- b.
# query(c).
# """)

formula = LogicFormula.create_from(program)
print("PROLOG:")
print(formula.to_prolog(), "\n============================")

cnf = CNF.create_from(formula)
print("CNF:")
print(cnf.to_dimacs(weighted=True, names=True), "\n============================")

ddnnf = DDNNF.create_from(cnf)
print("EVALUATION:")
print(ddnnf.evaluate(), "\n============================")
