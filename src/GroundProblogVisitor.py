"""
A visitor for parse trees of ground Problog programs that builds a GroundProblog object.
"""
from sys import exc_info
from six import reraise
from parsimonious import NodeVisitor, VisitationError, UndefinedLabel
from GroundProblog import *


# noinspection PyAbstractClass,PyMethodMayBeStatic
class GroundProblogVisitor(NodeVisitor):
    def visit(self, node):
        """Walk a parse tree, transforming it into another representation."""
        # Do nothing for following expressions
        skip_nodes = ["_", "dot", "comma", "semicolon", "lparen", "rparen",
                         "slash", "doublecolon", "turnstile", "negation"]
        if node.expr_name in skip_nodes:
            return

        method = getattr(self, 'visit_' + node.expr_name, self.generic_visit)

        # Call that method, and show where in the tree it failed if it blows up.
        try:
            return method(node, [self.visit(n) for n in node])
        except (VisitationError, UndefinedLabel):
            # Don't catch and re-wrap already-wrapped exceptions.
            raise
        except self.unwrapped_exceptions:
            raise
        except Exception:
            # Catch any exception, and tack on a parse tree so it's easier to
            # see where it went wrong.
            exc_class, exc, tb = exc_info()
            reraise(VisitationError, VisitationError(exc, exc_class, node), tb)

    def visit_program(self, node, visited_children):
        print("visit_program", visited_children)
        print('\n====================================================\n')
        return GroundProblog(visited_children[1])

    def visit_clauses(self, node, visited_children):
        print("visit_clauses", visited_children)
        return visited_children

    def visit_clause(self, node, visited_children):
        print("visit_clause", visited_children)
        return visited_children[0]

    def visit_predicate(self, node, visited_children):
        print("visit_predicate", visited_children)
        return visited_children[0]

    def visit_rule(self, node, visited_children):
        print("visit_rule", visited_children)
        return Rule(visited_children[0], visited_children[2])

    def visit_rule_body(self, node, visited_children):
        print("visit_rule_body", visited_children)
        return visited_children[0]

    def visit_conjunction(self, node, visited_children):
        print("visit_conjunction", visited_children)
        if visited_children[1] is not None:
            if isinstance(visited_children[1], list):
                return [visited_children[0]] + visited_children[1]
            else:
                return [visited_children[0], visited_children[1]]
        else:
            return visited_children[0]

    def visit_conjunction_opt(self, node, visited_children):
        exists_conjunction = len(visited_children) != 0
        print("visit_conjunction_opt", visited_children, exists_conjunction)
        return visited_children[0] if exists_conjunction else None

    def visit_conjunction_more(self, node, visited_children):
        print("visit_conjunction_more", visited_children)
        return visited_children[1]

    def visit_prob_declss(self, node, visited_children):
        print("visit_prob_decls", visited_children)
        return ProbabilityPredicate(visited_children[0])

    def visit_prob_decls(self, node, visited_children):
        print("visit_prob_decls", visited_children)
        if visited_children[1] is not None:
            if isinstance(visited_children[1], list):
                return [visited_children[0]] + visited_children[1]
            else:
                return [visited_children[0], visited_children[1]]
        else:
            return visited_children[0]

    def visit_prob_decls_opt(self, node, visited_children):
        exist_prob_decls = len(visited_children) != 0
        print("visit_prob_decls_opt", visited_children, exist_prob_decls)
        return visited_children[0] if exist_prob_decls else None

    def visit_prob_decls_more(self, node, visited_children):
        print("visit_prob_decls_more", visited_children)
        return visited_children[1]

    def visit_prob_decl(self, node, visited_children):
        print("visit_prob_decl", visited_children)
        return ProbabilityDeclaration(visited_children[0], visited_children[2])

    def visit_rule_predicate(self, node, visited_children):
        print("visit_rule_predicate", visited_children)
        return visited_children[0]

    def visit_term(self, node, visited_children):
        print("visit_term", visited_children)
        return Term(visited_children[1], visited_children[0], visited_children[2])

    def visit_negation_opt(self, node, visited_children):
        exists_negation = len(visited_children) != 0
        print("visit_negation_opt", visited_children, exists_negation)
        return exists_negation

    def visit_arguments_opt(self, node, visited_children):
        exist_arguments = len(visited_children) != 0
        print("visit_arguments_opt", visited_children, exist_arguments)
        return visited_children[0] if exist_arguments else None

    def visit_arguments(self, node, visited_children):
        print("visit_arguments", visited_children)
        return visited_children[1]

    def visit_arguments_list(self, node, visited_children):
        print("visit_arguments_list", visited_children)
        if visited_children[1] is not None:
            if isinstance(visited_children[1], list):
                return [visited_children[0]] + visited_children[1]
            else:
                return [visited_children[0], visited_children[1]]
        else:
            return visited_children[0]

    def visit_arguments_more_o(self, node, visited_children):
        exist_more_arguments = len(visited_children) != 0
        print("visit_arguments_more_o", visited_children, "more arguments exist: ", exist_more_arguments)
        return visited_children[0] if exist_more_arguments else None

    def visit_arguments_more(self, node, visited_children):
        print("visit_arguments_more", visited_children)
        return visited_children[1]

    def visit_probability(self, node, visited_children):
        print("visit_probability", visited_children)
        return visited_children[0]

    def visit_fraction(self, node, visited_children):
        print("visit_fraction", visited_children[0], visited_children[2], " => ", float(visited_children[0]) / float(visited_children[2]))
        return float(visited_children[0]) / float(visited_children[2])

    def visit_word(self, node, visited_children):
        print("visit_word", node.full_text[node.start:node.end])
        return node.full_text[node.start:node.end]

    def visit_number(self, node, visited_children):
        print("visit_number", int(node.full_text[node.start:node.end]))
        return int(node.full_text[node.start:node.end])

    def visit_decimal(self, node, visited_children):
        print("visit_decimal", float(node.full_text[node.start:node.end]))
        return float(node.full_text[node.start:node.end])

    def visit_meaninglessness(self, nodes, visited_children):
        pass