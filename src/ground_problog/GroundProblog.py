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

class Constraints:
    """Holds constraints for the FOL.
       These are things like A and B cannot be true at the same time
    """
    def __init__(self, notEquals):
        self.notEquals = notEquals

class GroundProblog:
    """ A ground problog program is a collection of clauses.
    A clause can be a fact (represented by just a Term here), a  Rule, or a ProbabilityPredicate.
    """
    def __init__(self, clauses, constraints=None):
        self.clauses = clauses
        self.constraints = [] if constraints is None else constraints

    def __str__(self):
        return ".\n".join(map(str, self.clauses)) + "."

    def get_facts(self):
        return [c for c in self.clauses if isinstance(c, Term) and c.name != "query" and c.name != "evidence"]

    def get_queries(self):
        # Queries have only 1 argument TODO: check this again
        return [c.arguments[0] for c in self.clauses if isinstance(c, Term) and c.name == "query"]

    def get_evidence(self):
        return [c.arguments[0] for c in self.clauses if isinstance(c, Term) and c.name == "evidence"]

    def get_rules(self):
        return [c for c in self.clauses if isinstance(c, Rule)]

    def get_probabilistic_annotations(self):
        return [c for c in self.clauses if isinstance(c, ProbabilisticAnnotation)]

    def get_constraints(self):
        return self.constraints

    def preprocess_ground(self):
        # Convert AD's to have heads with no probability
        new_program = self.convert_ad()

        # Return
        return new_program

    def convert_ad(self):
        # For each head in an ad:
        new_clauses = []
        # First get the probabilities from AD's and add new facts
        head_count = {}
        constraints = []
        for clause in self.clauses:
            if type(clause) is ProbabilisticAnnotation:

                # For each head in the annotation
                for head in clause.heads:
                    # We have a body
                    if head.name not in head_count:
                        head_count[head.name] = 0

                    if clause.body:
                        fake_head = "p_{}_{}".format(head.name, head_count[head.name])
                        head_count[head.name] += 1

                        fake_head_term = Term(fake_head, probability=head.probability)
                        new_clauses.append(fake_head_term)

                        # Create a new head with no weights
                        new_head_wo_prob = Term(head.name)

                        new_rule = Rule(new_head_wo_prob, clause.body + [fake_head_term])
                        new_clauses.append(new_rule)
                    else:
                        new_clauses.append(clause)

                if len(clause.heads) > 1:
                    constraints.append(clause.heads)

            else:
                # Nothing to change addd it to our new clauses
                new_clauses.append(clause)
        return GroundProblog(new_clauses, Constraints(constraints))