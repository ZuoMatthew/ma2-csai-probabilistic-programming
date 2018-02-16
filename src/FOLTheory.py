"""
A (limited) representation for First Order Logic theories.

Theories are collections of formulas. A formula is built out of atoms using universal and existential quantifiers
and the usual logical connectives negation, conjunction, disjunction, implication, biconditional.
"""


class Term:
    """ A term is a variable, a constant, or a functor applied on terms. """


class Atom:
    """ An atom is of the form p(t_1, ..., t_n) where p is a predicate of arity n and the t_i are terms. """
    def __init__(self, predicate, terms):
        self.predicate = predicate
        self.terms = terms
        self.arity = len(terms)

    def __str__(self):
        out = self.predicate
        if self.arity > 0:
            out += "(" + ", ".join([str(term) for term in self.terms]) + ")"
        return out

    def __eq__(self, other):
        return self.predicate == other.predicate and self.terms == other.terms

    @staticmethod
    def create_from_problog_term(term):
        arguments = []
        if len(term.arguments):
            arguments = [Atom.create_from_problog_term(arg) for arg in term.arguments]

        atom = Atom(predicate=term.name, terms=arguments)
        return Negation(atom) if term.negation else atom


class LogicFormula:
    """ Abstract class that represents a logical formula? """


class Negation(LogicFormula):
    """ Represents the logical connective '¬'. """
    def __init__(self, formula):
        self.formula = formula


class Conjunction(LogicFormula):
    """ Represents the logical connective '∧'. """
    def __init__(self, formulas):
        self.formulas = formulas

    def __str__(self):
        return "(" + " ∧ ".join([str(formula) for formula in self.formulas]) + ")"


class Disjunction(LogicFormula):
    """ Represents the logical connective '∨'. """
    def __init__(self, formulas):
        self.formulas = formulas

    def add_formula(self, formula):
        self.formulas.append(formula)

    def __str__(self):
        return "(" + " ∨ ".join([str(formula) for formula in self.formulas]) + ")"


class Biconditional(LogicFormula):
    """ Represents the logical connective '↔'. E.g. "w ↔ r ∨ s" """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def to_cnf(self):
        """ Convert this formula to a Conjunctive Normal Form. """
        return ""

    def __str__(self):
        return "(" + str(self.lhs) + " ↔ " + str(self.rhs) + ")"


class FOLTheory:
    """
    A FOL theory is a set of formulas that implicitly form a conjunction.
    """
    def __init__(self, formulas=[]):
        self.formulas = formulas

    def __str__(self):
        return "\n".join([str(formula) for formula in self.formulas])

    def add_formula(self, formula):
        self.formulas.append(formula)

    def extend_biconditional_disjunction(self, head, body):
        """ Finds a biconditional formula which has head as its lhs and extends its rhs with body.
        Creates a new biconditional if one is not found.
        """
        i = next((i for (i, v) in enumerate(self.formulas) if isinstance(v, Biconditional) and v.lhs == head), -1)

        if i != -1:
            # if biconditional with correct lhs has been found, extend the disjunction in the rhs
            self.formulas[i].rhs.add_formula(body)
        else:
            # otherwise, add a new biconditional to the formulas
            self.add_formula(Biconditional(head, Disjunction([body])))

    def to_cnf(self):
        return ""

    @staticmethod
    def create_from_problog(ground_problog):
        """ Creates a FOLTheory from a GroundProblog instance. """
        print("Converting program to FOL Theory:")
        theory = FOLTheory()

        # Problog facts can just be converted to FOL Atoms
        for fact in ground_problog.get_facts():
            theory.add_formula(Atom.create_from_problog_term(fact))

        # Problog rules are converted to FOL formulas by applying Clark's completion. This is done by grouping rule
        # bodies of rules with equal heads into disjunctions.
        rules = {}
        for rule in ground_problog.get_rules():
            head = Atom.create_from_problog_term(rule.head)
            body_atoms = [Atom.create_from_problog_term(term) for term in rule.body]
            body = Conjunction(body_atoms) if len(body_atoms) > 1 else body_atoms[0]
            theory.extend_biconditional_disjunction(head, body)

        # convert rules to logic formulas
        for rule in rules:
            theory.add_formula(Biconditional(rule, rules[rule]))

        return theory
