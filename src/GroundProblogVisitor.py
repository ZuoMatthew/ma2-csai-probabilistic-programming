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
        if node.expr_name in ["_", "end_clause", "comment", "lparen", "rparen"]:
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
        print("visit_program", visited_children, type(visited_children), type(node), node)

    def visit_clauses(self, node, visited_children):
        print("visit_clauses", visited_children, type(visited_children), type(node), node)

    def visit_clause(self, node, visited_children):
        print("visit_clause", visited_children, type(visited_children), type(node), node)

    def visit_newlines(self, node, visited_children):
        print("visit_newlines", visited_children, type(visited_children), type(node), node)

    def visit_negation_opt(self, node, visited_children):
        print("visit_negation", visited_children, type(visited_children), type(node), node)

    def visit_meaninglessness(self, nodes, visited_children):
        pass

    def visit_word(self, node, visited_children):
        print("visit_word", visited_children, type(visited_children), type(node), node)
        return "a word"

    def visit_arguments_opt(self, node, visited_children):
        print("visit_arguments_opt", visited_children, type(visited_children), type(node), node)

    def visit_arguments(self, node, visited_children):
        print("visit_arguments", visited_children, type(visited_children), type(node), node)

    def visit_term(self, node, visited_children):
        print("visit_term", visited_children, type(visited_children), type(node), node)

    def visit_fact(self, node, visited_children):
        print("visit_fact", visited_children, type(visited_children), type(node), node)

    def visit_predicate(self, node, visited_children):
        print("visit_predicate", visited_children, type(visited_children), type(node), node)
