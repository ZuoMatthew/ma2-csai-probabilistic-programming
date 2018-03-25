"""
This file defines classes that are used to build GroundProblog instances that represent ground problog programs.
"""

class Clause:
    """ Abstract class that represents a clause? """


class Term(Clause):
    """ A term has a name, can be negated, and possibly has arguments. """
    def __init__(self, name, negation=False, arguments=None, probability=1.0):
        self.name = name
        self.negation = negation
        self.arguments = arguments if arguments is not None else []
        self.probability = probability

    def __str__(self):
        out = (str(self.probability) + "::") if self.probability != 1.0 else ""
        out += ("\+" if self.negation else "") + self.name
        if len(self.arguments):
            out += "(" + ",".join(map(str, self.arguments)) + ")"
        return out


class Rule(Clause):
    """ A rule has a head and a body.
    The head is a term. The body can only be a term or a conjunction of terms in the case of ground problog.
    """
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __str__(self):
        out = str(self.head) + " :- " + ", ".join(map(str, self.body))
        return out


class ProbabilisticAnnotation(Clause):
    """ A collection of probabilistic heads (terms) with optionally a rule body. """
    def __init__(self, heads, body=None):
        self.heads = heads
        self.body = body if body is not None else []

    def __str__(self):
        out = "; ".join(map(str, self.heads))
        if len(self.body):
            out += " :- " + ", ".join(map(str, self.body))
        return out


class GroundProblog:
    """ A ground problog program is a collection of clauses.
    A clause can be a fact (represented by just a Term here), a  Rule, or a ProbabilityPredicate.
    """
    def __init__(self, clauses):
        self.clauses = clauses

    def __str__(self):
        return ".\n".join(map(str, self.clauses)) + "."

    def get_facts(self):
        return [c for c in self.clauses if isinstance(c, Term) and c.name != "query"]

    def get_queries(self):
        # Queries have only 1 argument TODO: check this again
        return [c.arguments[0] for c in self.clauses if isinstance(c, Term) and c.name == "query"]

    def get_rules(self):
        return [c for c in self.clauses if isinstance(c, Rule)]

    def get_probabilistic_annotations(self):
        return [c for c in self.clauses if isinstance(c, ProbabilisticAnnotation)]
