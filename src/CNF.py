import FOLTheory


class Literal:
    """ A literal of a CNF formula. """

    def __init__(self, name, negated=False, weight=1):
        self.name = name
        self.negated = negated
        self.weight = weight
        self.dimacs_int = None

    def __str__(self):
        return (str(self.weight)+"::" if self.weight != 1 else "") + ("-" if self.negated else "") + self.name

    def __eq__(self, other):
        return self.name == other.name and self.negated == other.negated and self.weight == other.weight


# return sorted(self.d.items(), key=lambda kv: kv[1])
class CNF:
    """ A formula in Conjunctive Normal Form with support for weights. """

    def __init__(self, literals=None, clauses=None, queries=None):
        # Dictionary of all the literals that are used in the clauses.
        self.literals = literals if literals is not None else {}
        # List of lists of Literal, which represents a conjunction of disjunctions of literals.
        self.clauses = clauses if clauses is not None else []
        # List of Literal.
        self.queries = queries if queries is not None else []

    def __str__(self):
        out = "Literals ({}):\n\t".format(len(self.get_literals()))
        out += "\n\t".join(map(str, self.get_literals()))

        if len(self.clauses):
            out += "\nClauses ({}):\n\t".format(len(self.clauses))
            out += "\n\t".join([" ∨ ".join(map(str, disjunction)) for disjunction in self.clauses])

        if len(self.queries):
            out += "\nQueries ({}):\n\t".format(len(self.queries))
            out += "\n\t".join(map(str, self.queries))

        return out

    def get_or_add_literal(self, literal):
        if not isinstance(literal, Literal):
            raise Exception("Adding literal of wrong type")
        
        if literal.name not in self.literals:
            literal.dimacs_int = len(self.literals) + 1
            self.literals[literal.name] = literal
            
        return self.literals[literal.name]

    def get_literals(self):
        return sorted(self.literals.values(), key=lambda lit: lit.dimacs_int)

    def add_clause(self, clause):
        if not isinstance(clause, list):
            raise Exception("Adding clause of wrong type")
        
        for lit in clause:
            if not isinstance(lit, Literal):
                raise Exception("Adding clause with wrong type of literal")
            lit.dimacs_int = self.get_or_add_literal(lit).dimacs_int
            
        self.clauses.append(clause)
        return clause

    def add_query(self, query):
        if not isinstance(query, Literal):
            raise Exception("Adding query of wrong type")

        query.dimacs_int = self.get_or_add_literal(query).dimacs_int
        self.queries.append(query)
        return query

    def get_queries_with_dimacs_numbers(self):
        return [(lit, lit.dimacs_int) for lit in self.queries]

    def to_dimacs(self):
        """ Converts the CNF to a dimacs format that can be parsed by the minic2d package."""
        literals = self.get_literals()

        # Add a comment to check assignments of numbers to literals
        header = "p cnf {} {}\n".format(len(literals), len(self.clauses))
        comment = "\n".join(["c {:>2}  {}".format(l.dimacs_int, l.name) for l in literals]) + "\n"
        comment += "c QUERIES: " + ", ".join([str(l.dimacs_int) for l in self.queries]) + "\n"

        weights = "c weights "
        weights += " ".join(["{} {}".format(l.weight, 1 - l.weight) for l in literals]) + "\n"

        dimacs = ""
        for disjunction in self.clauses:
            disjunction_literals = ["{}{}".format("-" if l.negated else "", l.dimacs_int) for l in disjunction]
            dimacs += " ".join(disjunction_literals) + " 0"

            if disjunction != self.clauses[-1]:
                dimacs += "\n"

        return weights + header + comment + dimacs

    @staticmethod
    def create_from_fol_theory(theory):
        cnf = CNF()

        for formula in theory.to_cnf().formulas:
            # A formula in CNF consists of literals or of disjunctions of literals
            if isinstance(formula, FOLTheory.Atom):
                lit = Literal(name=formula.str_no_probability(), negated=False, weight=formula.probability)
                cnf.get_or_add_literal(lit)

            elif isinstance(formula, FOLTheory.Conjunction):
                for f in formula.formulas:
                    if isinstance(f, FOLTheory.Disjunction):
                        clause = []
                        for ff in f.formulas:
                            if isinstance(ff, FOLTheory.Negation):
                                clause.append(Literal(str(ff.formula), True, ff.formula.probability))
                            else:
                                clause.append(Literal(str(ff), False, ff.probability))
                        cnf.add_clause(clause)
                    else:
                        raise Exception("Unexpected formula type in FOL CNF Conjunction:", type(f))

            else:
                raise Exception("Unexpected formula type in FOL CNF:", type(formula))

        for query in theory.get_queries():
            cnf.add_query(Literal(str(query)))

        return cnf
