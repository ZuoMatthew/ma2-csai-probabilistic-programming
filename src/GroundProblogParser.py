"""
A parser for ground ProbLog programs.
"""

from parsimonious.grammar import Grammar
from GroundProblogVisitor import GroundProblogVisitor
from FOLTheory import FOLTheory


def file_to_string(filename):
    with open(filename) as input_file:
        return input_file.read()


class GroundProblogParser:
    def __init__(self):
        self._visitor = GroundProblogVisitor(logging=True)

    def _grammar(self):
        # A PEG grammar for ground Problog. It is written in a very weird way
        # in order to make the visiting of the parse tree work.
        return Grammar(r"""
            program          = _ clauses
            clauses          = clause*
            clause           = predicate dot
            predicate        = prob_declss / rule / term
            
            rule             = term turnstile rule_body
            rule_body        = conjunction / term
            conjunction      = term conjunction_opt
            conjunction_opt  = conjunction_more?
            conjunction_more = comma conjunction

            prob_declss      = prob_decls _
            prob_decls       = prob_decl prob_decls_opt
            prob_decls_opt   = prob_decls_more?
            prob_decls_more  = semicolon prob_decls
            prob_decl        = prob_rule / prob_fact
            prob_rule        = probability doublecolon rule
            prob_fact        = probability doublecolon term

            term             = negation_opt word arguments_opt
            negation_opt     = negation?
            arguments_opt    = arguments?
            arguments        = lparen arguments_list rparen
            arguments_list   = term arguments_more_o
            arguments_more_o = arguments_more?
            arguments_more   = comma arguments_list
            
            probability      = decimal / fraction
            fraction         = number slash number
            word             = ~"[a-zA-Z0-9_']+"
            number           = ~"[0-9]*"
            decimal          = ~"[0-9]*\.[0-9]*"
            dot              = _ "." _
            comma            = _ "," _
            semicolon        = _ ";" _
            lparen           = _ "(" _
            rparen           = _ ")" _
            slash            = _ "/" _
            doublecolon      = _ "::" _
            turnstile        = _ ":-" _
            negation         = _ "\+" _
            
            _                = meaninglessness*
            meaninglessness  = ~r"\s+"
        """)

    def parse(self, program):
        """ Parses a ground problog program and returns the root node of the parse tree. """
        return self._grammar().parse(program)

    def parse_tree_to_problog(self, root_node):
        """ Visits a ground problog program's parse tree and
        returns a GroundProblog object that represents the program. """
        return self._visitor.visit(root_node)

    def parse_to_CNF(self, program):
        """ Converts a ground problog program to its CNF representation """
        # parse the program
        root_node = self.parse(program)
        print("Parse tree:")
        print(root_node)
        print("\n====================================================\n")

        # build the GroundProblog object
        ground_problog = self.parse_tree_to_problog(root_node)
        print("Program")
        print(ground_problog)
        print("\n====================================================\n")

        # convert the GroundProblog to a FOLTheory
        fol_theory = FOLTheory.create_from_problog(ground_problog)
        print("FOL theory:")
        print(fol_theory)
        print("\n====================================================\n")

        # convert the LogicFormula to its CNF representation
        """
        Converting LP rules to CNF is not simply a syntactical matter of rewriting the rules in the appropriate form. 
        The point is that the rules and the CNF are to be interpreted according to a different semantics. (LP versus 
        FOL). The rules under LP semantics (with Closed World Assumption) should be equivalent to the CNF under FOL 
        semantics (without CWA).
        """
        cnf = fol_theory.to_cnf()
        print("CNF:")
        print(cnf)
        return cnf


parser = GroundProblogParser()
program = file_to_string("files/test.grounded.pl")
cnf = parser.parse_to_CNF(program)
