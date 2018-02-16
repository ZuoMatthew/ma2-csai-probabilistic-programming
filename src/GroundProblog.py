"""
This file defines classes that are used to build GroundProblog instances that represent ground problog programs.
"""

class Term:
    """ A term has a name, can be negated, and possibly has arguments. """
    def __init__(self, name, negation, arguments):
        self.name = name
        self.negation = negation
        if isinstance(arguments, list):
            self.arguments = arguments
        else:
            self.arguments = [arguments]

    def __str__(self):
        out = ""
        if self.negation:
            out += "\+"
        out += self.name
        if self.arguments[0] is not None:
            out += "("
            for i in range(0, len(self.arguments)):
                out += str(self.arguments[i])
                if i != len(self.arguments)-1:
                    out += ","
            out += ")"
        return out


class Rule:
    """ A rule has a head and a body. The body can only be a term or a conjunction of terms
    in the case of ground problog. """
    def __init__(self, head, body):
        self.head = head
        if isinstance(body, list):
            self.body = body
        else:
            self.body = [body]

    def __str__(self):
        out = str(self.head) + " :- "
        for i in range(0, len(self.body)):
            out += str(self.body[i])
            if i != len(self.body)-1:
                out += ", "
        return out


class ProbabilityDeclaration:
    """ Represents a predicate that has a probability assigned to it. """
    def __init__(self, probability, predicate):
        self.probability = probability
        self.predicate = predicate

    def __str__(self):
        out = str(self.probability) + "::" + str(self.predicate)
        return out


class ProbabilityPredicate:
    """ A collection of ProbabilityDeclarations. """
    def __init__(self, declarations):
        if isinstance(declarations, list):
            self.declarations = declarations
        else:
            self.declarations = [declarations]

    def __str__(self):
        out = ""
        for i in range(0, len(self.declarations)):
            out += str(self.declarations[i])
            if i != len(self.declarations)-1:
                out += "; "
        return out


class GroundProblog:
    """ A ground problog program is a collection of clauses. """
    def __init__(self, clauses):
        self.clauses = clauses

    def __str__(self):
        return ".\n".join([str(clause) for clause in self.clauses]) + "."
