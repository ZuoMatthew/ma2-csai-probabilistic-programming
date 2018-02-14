"""
A visitor for parse trees of ground Problog programs that builds CNF representations of the programs.
"""
from sys import exc_info
from six import reraise
from parsimonious import NodeVisitor, VisitationError, UndefinedLabel


# noinspection PyAbstractClass,PyMethodMayBeStatic
class GroundProblogVisitor(NodeVisitor):
    def visit(self, node):
        """Walk a parse tree, transforming it into another representation."""
        # Do nothing for following expressions
        nodes_to_skip = ["_", "dot", "comma", "semicolon", "lparen", "rparen",
                         "slash", "doublecolon", "turnstile", "negation"]
        if node.expr_name in nodes_to_skip:
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

    def visit_clauses(self, node, visited_children):
        print("visit_clauses", visited_children)

    def visit_clause(self, node, visited_children):
        print("visit_clause", visited_children)

    def visit_predicate(self, node, visited_children):
        print("visit_predicate", visited_children)

    def visit_fact(self, node, visited_children):
        print("visit_fact", visited_children)

    def visit_rule(self, node, visited_children):
        print("visit_rule", visited_children)

    def visit_rule_body(self, node, visited_children):
        print("visit_rule_body", visited_children)

    def visit_conjunction(self, node, visited_children):
        print("visit_conjunction", visited_children)

    def visit_conjunction_opt(self, node, visited_children):
        print("visit_conjunction_opt", visited_children)

    def visit_conjunction_more(self, node, visited_children):
        print("visit_conjunction_more", visited_children)

    def visit_prob_decls(self, node, visited_children):
        print("visit_prob_decls", visited_children)

    def visit_prob_decls_opt(self, node, visited_children):
        print("visit_prob_decls_opt", visited_children)

    def visit_prob_decls_more(self, node, visited_children):
        print("visit_prob_decls_more", visited_children)

    def visit_prob_decl(self, node, visited_children):
        print("visit_prob_decl", visited_children)

    def visit_rule_predicate(self, node, visited_children):
        print("visit_rule_predicate", visited_children)

    def visit_term(self, node, visited_children):
        print("visit_term", visited_children)

    def visit_negation_opt(self, node, visited_children):
        print("visit_negation", visited_children)

    def visit_arguments_opt(self, node, visited_children):
        print("visit_arguments_opt", visited_children)

    def visit_arguments(self, node, visited_children):
        print("visit_arguments", visited_children)

    def visit_arguments_list(self, node, visited_children):
        print("visit_arguments_list", visited_children)

    def visit_arguments_more_o(self, node, visited_children):
        print("visit_arguments_more_o", visited_children)

    def visit_arguments_more(self, node, visited_children):
        print("visit_arguments_more", visited_children)

    def visit_probability(self, node, visited_children):
        print("visit_probability", visited_children)

    def visit_fraction(self, node, visited_children):
        print("visit_fraction", visited_children)

    def visit_word(self, node, visited_children):
        print("visit_word", visited_children)
        return "a word"

    def visit_number(self, node, visited_children):
        print("visit_decimal", visited_children)

    def visit_decimal(self, node, visited_children):
        print("visit_decimal", visited_children)

    def visit_meaninglessness(self, nodes, visited_children):
        pass