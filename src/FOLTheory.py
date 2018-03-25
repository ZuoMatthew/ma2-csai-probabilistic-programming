"""
A limited representation for First Order Logic theories with weighted atoms.

'Theories are collections of formulas. A formula is built out of atoms using universal and existential quantifiers
and the usual logical connectives negation, conjunction, disjunction, implication, equivalence.'
-- paper
"""


class LogicFormula:
    """ Abstract class that represents a logical formula """

    def to_cnf(self):
        raise NotImplementedError


class Atom(LogicFormula):
    """ An atom is of the form p(t_1, ..., t_n) where p is a predicate of arity n and the t_i are terms. """

    def __init__(self, predicate, terms=None, probability=1):
        self.predicate = predicate
        self.terms = terms if terms is not None else []
        self.arity = len(self.terms)
        self.probability = probability

    def __str__(self):
        out = ""
        if self.probability != 1:
            out += str(self.probability) + "::"
        out += self.predicate
        if self.arity > 0:
            out += "(" + ", ".join(map(str, self.terms)) + ")"
        return out

    def __eq__(self, other):
        return isinstance(other, Atom) and self.predicate == other.predicate and self.terms == other.terms

    def str_no_probability(self):
        out = self.predicate
        if self.arity > 0:
            out += "(" + ", ".join(map(str, self.terms)) + ")"
        return out

    def to_cnf(self):
        return self

    @staticmethod
    def create_from_problog_term(term):
        arguments = []
        if len(term.arguments):
            arguments = [Atom.create_from_problog_term(arg) for arg in term.arguments]

        atom = Atom(predicate=term.name, terms=arguments, probability=term.probability)
        return Negation(atom) if term.negation else atom


class Negation(LogicFormula):
    """ Represents the logical connective '¬'. """

    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return "¬(" + str(self.formula) + ")"

    def __eq__(self, other):
        return isinstance(other, Negation) and self.formula == other.formula

    def to_cnf(self):
        """ Convert this formula to Conjunctive Normal Form. """
        # If formula is of form ¬(A) where A is an Atom, return A
        if isinstance(self.formula, Atom):
            return self

        # If formula is of form ¬(¬P), return P.to_cnf()
        elif isinstance(self.formula, Negation):
            return self.formula.formula.to_cnf()

        # If formula is of form ¬(P ∧ ... ∧ Q), return (¬P ∨ ... ∨ ¬Q).to_cnf() (de Morgan's Law)
        elif isinstance(self.formula, Conjunction):
            negated_subformulas = [Negation(f) for f in self.formula.formulas]
            return Disjunction(negated_subformulas).to_cnf()

        # If formula is of form ¬(P ∨ ... ∨ Q), return (¬P ∧ ... ∧ ¬Q).to_cnf() (de Morgan's Law)
        elif isinstance(self.formula, Disjunction):
            negated_subformulas = [Negation(f) for f in self.formula.formulas]
            return Conjunction(negated_subformulas).to_cnf()

        else:
            raise Exception("Unexpected formula type")


class Conjunction(LogicFormula):
    """ Represents the logical connective '∧'. """

    def __init__(self, formulas):
        self.formulas = []
        # Lift nested Conjunctions' formulas up into this one.
        for f in formulas:
            if isinstance(f, Conjunction):
                self.formulas += f.formulas
            else:
                self.formulas.append(f)

    def __str__(self):
        return "(" + " ∧ ".join(map(str, self.formulas)) + ")"

    def __eq__(self, other):
        if not isinstance(other, Conjunction):
            return False
        for f in self.formulas:
            if f not in other.formulas:
                return False
        for f in other.formulas:
            if f not in self.formulas:
                return False
        return True

    def to_cnf(self):
        """ Convert this formula to Conjunctive Normal Form. """
        if len(self.formulas) == 1:
            # If there is just one formula in the Conjunction, then return the CNF of that formula.
            return self.formulas[0].to_cnf()
        else:
            # Formula is of form (P ∧ ... ∧ Q)
            # P.to_cnf() must have the form P1 ∧ P2 ∧ ... ∧ Pm
            # Q.to_cnf() must have the form Q1 ∧ Q2 ∧ ... ∧ Qn
            # where all Pi and Qi are disjunctions of literals. => return P1 ∧ ... ∧ Pm ∧ Q1 ∧ ... ∧ Qm
            return Conjunction([f.to_cnf() for f in self.formulas])  # (P.to_cnf() ∧ ... ∧ Q.to_cnf())


class Disjunction(LogicFormula):
    """ Represents the logical connective '∨'. """

    def __init__(self, formulas):
        self.formulas = []
        # Lift nested Disjunction' formulas up into this one.
        for f in formulas:
            if isinstance(f, Disjunction):
                self.formulas += f.formulas
            else:
                self.formulas.append(f)

    def __str__(self):
        return "(" + " ∨ ".join(map(str, self.formulas)) + ")"

    def __eq__(self, other):
        if not isinstance(other, Disjunction):
            return False
        for f in self.formulas:
            if f not in other.formulas:
                return False
        for f in other.formulas:
            if f not in self.formulas:
                return False
        return True

    def to_cnf(self):
        """ Convert this formula to Conjunctive Normal Form. """
        if len(self.formulas) == 1:
            # If there is just one formula in the Disjunction, then return the CNF of that formula.
            return self.formulas[0].to_cnf()
        else:
            # Formula is of form (P ∨ ... ∨ Q)
            # P.to_cnf() must have the form P1 ∧ P2 ∧ ... ∧ Pm
            # Q.to_cnf() must have the form Q1 ∧ Q2 ∧ ... ∧ Qn
            # where all Pi and Qi are disjunctions of literals
            # We need a CNF formula equivalent to (P1 ∧ P2 ∧ ... ∧ Pm) ∨ (Q1 ∧ Q2 ∧ ... ∧ Qn)
            # => return (P1 ∨ Q1) ∧ (P1 ∨ Q2) ∧ ... ∧ (P1 ∨ Qn)
            #         ∧ (P2 ∨ Q1) ∧ (P2 ∨ Q2) ∧ ... ∧ (P2 ∨ Qn)
            #         ∧ ...
            #         ∧ (Pm ∨ Q1) ∧ (Pm ∨ Q1) ∧ ... ∧ (Pm ∨ Qn)
            # In other words, apply the distributive law where a disjunction occurs over a conjunction.
            formulas_cnf = [f.to_cnf() for f in self.formulas]

            if len([f for f in formulas_cnf if isinstance(f, Conjunction)]) == 0:
                # If there is no Conjunction in this Disjunction, the formula is already in CNF
                return Disjunction(formulas_cnf)

            # Build up the result as a Conjunction of Disjunctions
            result = Conjunction([formulas_cnf.pop(0)])
            while len(formulas_cnf) > 0:
                f = formulas_cnf.pop(0)
                f_formulas = [f] if isinstance(f, (Atom, Negation)) else f.formulas

                disjunctions = []
                for p in result.formulas:
                    for q in f_formulas:
                        disjunctions.append(Disjunction([p, q]))

                result = Conjunction(disjunctions)

            return result.to_cnf()


class Equivalence(LogicFormula):
    """ Represents the logical connective '↔'. E.g. "w ↔ r ∨ s" """

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "(" + str(self.lhs) + " ↔ " + str(self.rhs) + ")"

    def __eq__(self, other):
        return isinstance(other, Equivalence) and \
               (self.lhs == other.lhs and self.rhs == other.rhs or self.lhs == other.rhs and self.rhs == other.lhs)

    def to_cnf(self):
        """ Convert this formula to Conjunctive Normal Form. """
        # Formula is of form P ↔ Q
        a = Disjunction([self.lhs, Negation(self.rhs)])  # (P ∨ ¬Q)
        b = Disjunction([Negation(self.lhs), self.rhs])  # (¬P ∨ Q)
        return Conjunction([a, b]).to_cnf()              # ((P ∨ ¬Q) ∧ (¬P ∨ Q)).to_cnf()


class FOLTheory:
    """
    A FOL theory is a set of formulas that implicitly form a conjunction.
    """

    def __init__(self, formulas=None, queries=None):
        self.formulas = formulas if formulas is not None else []
        self.queries = queries if queries is not None else []

    def __str__(self):
        out = "Formulas ({}):\n\t".format(len(self.formulas))
        out += "\n\t".join(map(str, self.formulas))

        if len(self.queries):
            out += "\nQueries ({}):\n\t".format(len(self.queries))
            out += "\n\t".join(map(str, self.queries))

        return out

    def add_formula(self, formula):
        self.formulas.append(formula)

    def add_query(self, query):
        self.queries.append(query)

    def get_formulas(self):
        return self.formulas

    def get_queries(self):
        return self.queries

    def to_cnf(self):
        return FOLTheory([f.to_cnf() for f in self.formulas])

    @staticmethod
    def create_from_problog(ground_problog):
        """ Creates a FOLTheory from a GroundProblog instance. """
        theory = FOLTheory()

        # Problog facts can just be converted to FOL Atoms
        for fact in ground_problog.get_facts():
            theory.add_formula(Atom.create_from_problog_term(fact))

        for query in ground_problog.get_queries():
            theory.add_query(Atom.create_from_problog_term(query))

        # Problog rules are converted to FOL formulas by applying Clark's completion. This is done by grouping rule
        # bodies of rules with equal heads into disjunctions.
        rules = []  # a list of (head, body) tuples
        for rule in ground_problog.get_rules():
            # Create the corresponding head and body as FOL formulas.
            head = Atom.create_from_problog_term(rule.head)
            body_atoms = [Atom.create_from_problog_term(term) for term in rule.body]
            body = Conjunction(body_atoms) if len(body_atoms) > 1 else body_atoms[0]

            # Add the rule in the rules list. If the rule already exists, extend the disjunction of its body.
            i = next((i for (i, (h, b)) in enumerate(rules) if h == head), -1)
            if i == -1:
                rules.append((head, body))
            else:
                rules[i] = (rules[i][0], Disjunction([rules[i][1], body]))

        for (head, body) in rules:
            theory.add_formula(Equivalence(head, body))

        return theory
