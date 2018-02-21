import FOLTheory


class Literal:
    """ A literal of a CNF formula. """
    def __init__(self, name, negated=False, weight=1, number=-1):
        self.name = name
        self.negated = negated
        self.weight = weight
        self.number = number

    def __str__(self):
        return ("-" if self.negated else "") + self.name

    def __eq__(self, other):
        return self.name == other.name and self.negated == other.negated and self.weight == other.weight


class CNF:
    """ A formula in Conjunctive Normal Form with support for weights. """
    def __init__(self, literals=None, clauses=None, queries=None):
        # Literals is a list of Literal.
        self.literals = literals if literals is not None else []
        # Clauses is a list of lists of Literal, which represents a conjunction of disjunctions of literals.
        self.clauses = clauses if clauses is not None else []
        # Queries is a list of Literal.
        self.queries = queries if queries is not None else []

    def __str__(self):
        out = "\n∧ ".join(map(str, self.literals))
        if len(self.clauses):
            out += "\n∧ " + "\n∧ ".join([" ∨ ".join(map(str, disjunction)) for disjunction in self.clauses])
        if len(self.queries):
            out += "\nQueries:\n" + "\n".join(map(str, self.queries))
        return out

    def add_literal(self, literal):
        if literal not in self.literals:
            literal.number = len(self.literals) + 1
            self.literals.append(literal)

    def add_clause(self, clause):
        self.clauses.append(clause)

    def add_query(self, query):
        self.queries.append(query)

    def to_dimacs(self):
        out = "p wcnf " + str(len(self.literals)) + " " + str(len(self.clauses)) + " SOMENUMBERHERE\n"
        out += "\n".join(["c " + str(lit.number) + " " + lit.name for lit in self.literals]) + "\n"

        for lit in self.literals:
            out += str(1 - lit.weight) + " -" + str(lit.number) + " 0\n"
            out += str(lit.weight) + " " + str(lit.number) + " 0\n"

        for disjunction in self.clauses:
            out += "SOMENUMBER "
            for literal in disjunction:
                lit = next((lit for lit in self.literals if lit == literal), None)
                if lit:
                    out += ("-" if lit.negated else "") + lit.number + " "
                else:
                    s = "Unknown literal '" + str(literal) + "' found in clause '" + " ∨ ".join(map(str, disjunction))
                    s += "' for CNF:\n" + str(self)
                    raise Exception(s)
            out += " 0\n"

        return out

    @staticmethod
    def create_from_fol_theory(theory):
        cnf = CNF()

        for formula in theory.to_cnf().formulas:
            # A formula in CNF consists of literals or of disjunctions of literals
            if isinstance(formula, FOLTheory.Atom):
                lit = Literal(str(formula), False, formula.probability)
                cnf.add_literal(lit)

            elif isinstance(formula, FOLTheory.Conjunction):
                for f in formula.formulas:
                    if isinstance(f, FOLTheory.Atom):
                        print("IS THIS POSSIBLE??????????????????????????????????????????? WHATAMGONNADOOOO ??????????")
                    elif isinstance(f, FOLTheory.Negation):
                        print("IS THIS POSSIBLE??????????????????????????????????????????? WHATAMGONNADOOOO ??????????")
                    elif isinstance(f, FOLTheory.Disjunction):
                        literals = []
                        for ff in f.formulas:
                            if isinstance(ff, FOLTheory.Negation):
                                literals.append(Literal(str(ff.formula), True, ff.formula.probability))
                            else:
                                literals.append(Literal(str(ff), False, ff.probability))
                        cnf.add_clause(literals)

            else:
                raise Exception("Unexpected formula type")

        for query in theory.get_queries():
            cnf.add_query(Literal(str(query)))

        return cnf
