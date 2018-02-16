"""
A (limited?) representation for First Order Logic theories.

Converting LP rules to CNF is not simply a syntactical matter of rewriting the rules in the appropriate form. The point
is that the rules and the CNF are to be interpreted according to a different semantics. (LP versus FOL). The rules
under LP semantics (with Closed World Assumption) should be equivalent to the CNF under FOL semantics (without CWA).
"""


class Term:
    """ A term is a variable, a constant, or a functor applied on terms. """


class Atom:
    """ An atom is of the form p(t_1, ..., t_n) where p is a predicate of arity n and the t_i are terms. """


class LogicFormula:
    """
    A formula is built out of atoms using universal and existential quantifiers and the usual logical connectives
    negation, conjunction, disjunction, implication, biconditional.
    """


class FOLTheory:
    """
    A FOL theory is a set of formulas that implicitly form a conjunction.
    """
    def __init__(self, formulas):
        self.formulas = formulas

    def __str__(self):
        out = "FOL Theory:"
        for formula in self.formulas:
            out += formula + "\n"
        return out

    def to_cnf(self):
        return ""

def create_from_problog(ground_problog):
    """ Creates a FOLTheory from a GroundProblog instance. """
    return FOLTheory([])
