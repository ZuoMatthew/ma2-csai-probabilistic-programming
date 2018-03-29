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
        out += self.str_no_prob()
        return out

    def str_no_prob(self):
        out = ("\+" if self.negation else "") + self.name
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
        return [c for c in self.clauses if isinstance(c, Term) and c.name != "query" and c.name != "evidence"]

    def get_queries(self):
        return [c.arguments[0] for c in self.clauses if isinstance(c, Term) and c.name == "query"]

    def get_evidence(self):
        return [c.arguments[0] for c in self.clauses if isinstance(c, Term) and c.name == "evidence"]

    def get_rules(self):
        return [c for c in self.clauses if isinstance(c, Rule)]

    def get_probabilistic_annotations(self):
        return [c for c in self.clauses if isinstance(c, ProbabilisticAnnotation)]

    def convert_ads_with_body_to_rules(self):
        """ Converts annotated disjunctions with rule bodies to normal rules.
        This is done by pulling the probabilities out to new probabilistic facts. A new normal rule is then created for
        each of the heads. Each new rule contains the new probabilistic fact that was created for it's head.
        The new probabilistic facts are then added in a new annotated disjunction without rule body, to keep the
        constraint that only one of the new rules can be true.
        """
        new_clauses = []
        head_count = {}

        for clause in self.clauses:
            if not isinstance(clause, ProbabilisticAnnotation):
                new_clauses.append(clause)

            else:
                # TODO: handle this case: 0.3::x. 0.7::a; 0.3::b: - x.evidence(a).query(a).query(b).
                # Should be possible by simply adding the new AD: 0.7::p_a_0 ; 0.3::p_b_0.
                if len(clause.body):
                    for head in clause.heads:
                        if head.str_no_prob() not in head_count:
                            head_count[head.str_no_prob()] = 0
                        else:
                            head_count[head.str_no_prob()] += 1
                        new_prob_fact_name = "p_{}_{}".format(head.str_no_prob(), head_count[head.str_no_prob()])

                        # Create the new probabilistic fact that hold the probability of the current head
                        new_prob_fact = Term(new_prob_fact_name, probability=head.probability)
                        new_clauses.append(new_prob_fact)

                        # Create a new head with no weights for the new normal rule
                        new_head_wo_prob = Term(head.name, arguments=head.arguments)
                        new_rule = Rule(new_head_wo_prob, clause.body + [new_prob_fact])
                        new_clauses.append(new_rule)
                else:
                    new_clauses.append(clause)

        return GroundProblog(new_clauses)

    def remove_duplicate_probabilistic_terms(self):
        return self