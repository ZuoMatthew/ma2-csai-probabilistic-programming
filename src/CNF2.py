import FOLTheory


class CNF:
    """
    A formula in Conjunctive Normal Form with support for weights.
    """
    def __init__(self, unit_clauses=[], clauses=[]):
        self.unit_clauses = unit_clauses
        self.clauses = clauses

    def __str__(self):
        return "\n∧ ".join([str(c) for c in self.clauses])

    def add_unit_clause(self, formula):
        self.unit_clauses.append(formula)

    def add_clause(self, formula):
        self.clauses.append(formula)

    @staticmethod
    def create_from_fol_theory(theory):
        cnf = CNF()

        for formula in theory.to_cnf().formulas:
            if isinstance(formula, (FOLTheory.Atom, FOLTheory.Negation)):
                cnf.add_unit_clause(formula)
            elif isinstance(formula, FOLTheory.Conjunction):
                cnf.add_clause(formula.formulas)
            else:
                raise Exception("Unexpected formula type")

        return cnf