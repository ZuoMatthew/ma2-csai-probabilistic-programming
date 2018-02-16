"""
A (limited) representation for First Order Logic theories.

Theories are collections of formulas. A formula is built out of atoms using universal and existential quantifiers
and the usual logical connectives negation, conjunction, disjunction, implication, equivalence.
"""


class Term:
    """ A term is a variable, a constant, or a functor applied on terms. """


class LogicFormula:
    """ Abstract class that represents a logical formula? """
    def to_cnf(self):
        return self


class Atom(LogicFormula):
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


class Negation(LogicFormula):
    """ Represents the logical connective '¬'. """
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return "¬(" + str(self.formula) + ")"

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
        self.formulas = formulas

    def __str__(self):
        return "(" + " ∧ ".join([str(f) for f in self.formulas]) + ")"

    def to_cnf(self):
        """ Convert this formula to Conjunctive Normal Form. """
        # Formula is of form (P ∧ ... ∧ Q)
        # P.to_cnf() must have the form P1 ∧ P2 ∧ ... ∧ Pm
        # Q.to_cnf() must have the form Q1 ∧ Q2 ∧ ... ∧ Qn
        # where all Pi and Qi are disjunctions of literals. => return P1 ∧ ... ∧ Pm ∧ Q1 ∧ ... ∧ Qm
        return Conjunction([f.to_cnf() for f in self.formulas])  # (P.to_cnf() ∧ ... ∧ Q.to_cnf())


class Disjunction(LogicFormula):
    """ Represents the logical connective '∨'. """
    def __init__(self, formulas):
        self.formulas = formulas

    def __str__(self):
        return "(" + " ∨ ".join([str(f) for f in self.formulas]) + ")"

    def add_formula(self, formula):
        self.formulas.append(formula)

    def to_cnf(self):
        """ Convert this formula to Conjunctive Normal Form. """
        # Formula is of form (P ∨ ... ∨ Q)
        # P.to_cnf() must have the form P1 ∧ P2 ∧ ... ∧ Pm
        # Q.to_cnf() must have the form Q1 ∧ Q2 ∧ ... ∧ Qn
        # where all Pi and Qi are disjunctions of literals
        # We need a CNF formula equivalent to (P1 ∧ P2 ∧ ... ∧ Pm) ∨ (Q1 ∧ Q2 ∧ ... ∧ Qn)
        # => return (P1 v Q1) ^ (P1 v Q2) ^ ... ^ (P1 v Qn)
        #         ^ (P2 v Q1) ^ (P2 v Q2) ^ ... ^ (P2 v Qn)
        #         ^ ...
        #         ^ (Pm v Q1) ^ (Pm v Q1) ^ ... ^ (Pm V Qn)
        # In other words, apply the distributive law where a disjunction occurs over a conjunction.
        if len(self.formulas) == 1:
            return self.formulas[0]
        else:
            p = self.formulas.pop(0).to_cnf()
            q = self.formulas.pop(0).to_cnf()
            p_formulas = [p] if isinstance(p, (Atom, Negation)) else p.formulas
            q_formulas = [q] if isinstance(q, (Atom, Negation)) else q.formulas

            formulas = []
            for f1 in p_formulas:
                for f2 in q_formulas:
                    formulas.append(Disjunction([f1, f2]))
            # create conjunction of new disjunctions
            conj = Conjunction(formulas)
            return Disjunction(self.formulas + [conj]).to_cnf()


class Equivalence(LogicFormula):
    """ Represents the logical connective '↔'. E.g. "w ↔ r ∨ s" """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "(" + str(self.lhs) + " ↔ " + str(self.rhs) + ")"

    def to_cnf(self):
        """ Convert this formula to Conjunctive Normal Form. """
        # Formula is of form P ↔ Q
        # a = Conjunction([self.lhs, self.rhs])                          # (P ∧ Q)
        # b = Conjunction([Negation(self.lhs), Negation(self.rhs)])      # (¬P ∧ ¬Q)
        # return Disjunction([a, b]).to_cnf()                            # ((P ∧ Q) ∨ (¬P ∧ ¬Q)).to_cnf()
        a = Disjunction([self.lhs, Negation(self.rhs)])                # (P ∨ ¬Q)
        b = Disjunction([Negation(self.lhs), self.rhs])                # (¬P ∨ Q)
        return Conjunction([a, b]).to_cnf()                            # ((P ∨ ¬Q) ∧ (¬P ∨ Q)).to_cnf()


class FOLTheory:
    """
    A FOL theory is a set of formulas that implicitly form a conjunction.
    """
    def __init__(self, formulas=[]):
        self.formulas = formulas

    def __str__(self):
        return "\n".join([str(f) for f in self.formulas])

    def add_formula(self, formula):
        self.formulas.append(formula)

    def to_cnf(self):
        return FOLTheory([f.to_cnf() for f in self.formulas])

    @staticmethod
    def create_from_problog(ground_problog):
        """ Creates a FOLTheory from a GroundProblog instance. """
        theory = FOLTheory()

        # Problog facts can just be converted to FOL Atoms
        for fact in ground_problog.get_facts():
            theory.add_formula(Atom.create_from_problog_term(fact))

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
                if isinstance(rules[i][1], Disjunction):
                    rules[i][1].add_formula(body)
                else:
                    rules[i] = (rules[i][0], Disjunction([rules[i][1], body]))

        for (head, body) in rules:
            theory.add_formula(Equivalence(head, body))

        return theory
