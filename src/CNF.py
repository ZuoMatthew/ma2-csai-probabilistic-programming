import FOLTheory
from util import IncrementingDict


class Literal:
    """ A literal of a CNF formula. """

    def __init__(self, name, negated=False, weight=1):
        self.name = name
        self.negated = negated
        self.weight = weight

    def __str__(self):
        return ("-" if self.negated else "") + self.name

    def __eq__(self, other):
        return self.name == other.name and self.negated == other.negated and self.weight == other.weight


class CNF:
    """ A formula in Conjunctive Normal Form with support for weights. """

    def __init__(self, literals=None, clauses=None, queries=None):
        # List of Literal.
        self.literals = literals if literals is not None else []
        # List of lists of Literal, which represents a conjunction of disjunctions of literals.
        self.clauses = clauses if clauses is not None else []
        # List of Literal.
        self.queries = queries if queries is not None else []
        # Dictionary that keeps track of the numbers that have been assigned to literals.
        self.dimacs_assignments = IncrementingDict()

    def __str__(self):
        out = "\n∧ ".join(map(str, self.literals))
        if len(self.clauses):
            out += "\n∧ " + "\n∧ ".join([" ∨ ".join(map(str, disjunction)) for disjunction in self.clauses])
        if len(self.queries):
            out += "\nQueries:\n" + "\n".join(map(str, self.queries))
        return out

    def add_literal(self, literal):
        if not isinstance(literal, Literal):
            raise Exception("Adding literal of wrong type")
        if literal not in self.literals:
            self.literals.append(literal)

    def add_clause(self, clause):
        if not isinstance(clause, list):
            raise Exception("Adding clause of wrong type")
        for lit in clause:
            if not isinstance(lit, Literal):
                raise Exception("Adding clause with wrong type of literal")
        self.clauses.append(clause)

    def add_query(self, query):
        self.queries.append(query)

    def get_queries_with_dimacs_numbers(self):
        return [(lit, self.dimacs_assignments.get(lit.name)) for lit in self.queries]

    def to_dimacs(self, to_minic2d=True):
        """ Converts the CNF to dimacs format that can be parsed by the minic2d or sdd packages."""
        dimacs = ""
        if to_minic2d:
            weights = "c weights "
            header = "p cnf {} {}\n".format(len(self.literals), len(self.clauses))
        else:
            weights = ""
            header = "p wcnf {} {} {}\n".format(len(self.literals), len(self.clauses), "SOMENUMBERHERE")

        for lit in self.literals:
            if to_minic2d:
                weights += "{} ".format(lit.weight)
                weights += "{} ".format(1 - lit.weight)
                self.dimacs_assignments.get(lit.name)
            else:
                dimacs += "{} -{} 0\n".format(1 - lit.weight, self.dimacs_assignments.get(lit.name))
                dimacs += "{} {} 0\n".format(lit.weight, self.dimacs_assignments.get(lit.name))
        weights += "\n"

        for disjunction in self.clauses:
            if not to_minic2d:
                dimacs += "WEIGHT? "

            for lit in disjunction:
                dimacs += "{}{} ".format("-" if lit.negated else "", self.dimacs_assignments.get(lit.name))

            dimacs += "0"
            if disjunction != self.clauses[-1]:
                dimacs += "\n"

        # Add a comment to check assignments of numbers to literals
        comment = "\n".join(["c {:>2}  {}".format(num, k) for k, num in self.dimacs_assignments.items()]) + "\n"
        comment += "c QUERIES: "
        comment += ", ".join([str(self.dimacs_assignments.get(lit.name)) for lit in self.queries]) + "\n"

        return weights + header + comment + dimacs

    @staticmethod
    def create_from_fol_theory(theory):
        cnf = CNF()

        for formula in theory.to_cnf().formulas:
            # A formula in CNF consists of literals or of disjunctions of literals
            if isinstance(formula, FOLTheory.Atom):
                lit = Literal(name=formula.str_no_probability(), negated=False, weight=formula.probability)
                cnf.add_literal(lit)

            elif isinstance(formula, FOLTheory.Conjunction):
                for f in formula.formulas:
                    if isinstance(f, FOLTheory.Disjunction):
                        literals = []
                        for ff in f.formulas:
                            if isinstance(ff, FOLTheory.Negation):
                                literals.append(Literal(str(ff.formula), True, ff.formula.probability))
                            else:
                                literals.append(Literal(str(ff), False, ff.probability))
                        cnf.add_clause(literals)
                    else:
                        raise Exception("Unexpected formula type in FOL CNF Conjunction:", type(f))

            else:
                raise Exception("Unexpected formula type in FOL CNF:", type(formula))

        for query in theory.get_queries():
            cnf.add_query(Literal(str(query)))

        return cnf
