"""
This file defines classes that are used to build GroundProblog instances that represent ground problog programs.
"""


class Term:
    """ A term has a name, can be negated, and possibly has arguments. """
    def __init__(self, name, negation, arguments):
        self.name = name
        self.negation = negation
        if arguments is None:
            self.arguments = []
        elif isinstance(arguments, list):
            self.arguments = arguments
        else:
            self.arguments = [arguments]

    def __str__(self):
        out = ("\+" if self.negation else "") + self.name
        if len(self.arguments):
            out += "(" + ",".join([str(arg) for arg in self.arguments]) + ")"
        return out


class Rule:
    """ A rule has a head and a body.
    The head is a term. The body can only be a term or a conjunction of terms in the case of ground problog.
    """
    def __init__(self, head, body):
        self.head = head
        if isinstance(body, list):
            self.body = body
        else:
            self.body = [body]

    def __str__(self):
        out = str(self.head) + " :- "
        if len(self.body):
            out += ", ".join([str(term) for term in self.body])
        return out


class ProbabilityDeclaration:
    """ Represents a predicate that has a probability assigned to it. """
    def __init__(self, probability, predicate):
        self.probability = probability
        self.predicate = predicate

    def __str__(self):
        return str(self.probability) + "::" + str(self.predicate)


class ProbabilityPredicate:
    """ A collection of ProbabilityDeclarations. """
    def __init__(self, declarations):
        if isinstance(declarations, list):
            self.declarations = declarations
        else:
            self.declarations = [declarations]

    def __str__(self):
        return "; ".join([str(declaration) for declaration in self.declarations])


class GroundProblog:
    """ A ground problog program is a collection of clauses.
    A clause can be a fact (represented by just a Term here), a  Rule, or a ProbabilityPredicate.
    """
    def __init__(self, clauses):
        self.clauses = clauses

    def get_facts(self):
        return [clause for clause in self.clauses if isinstance(clause, Term)]

    def get_rules(self):
        return [clause for clause in self.clauses if isinstance(clause, Rule)]

    def get_probability_predicates(self):
        return [clause for clause in self.clauses if isinstance(clause, ProbabilityPredicate)]

    def __str__(self):
        return ".\n".join([str(clause) for clause in self.clauses]) + "."
