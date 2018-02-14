"""
A parser for ground ProbLog programs.
"""

from parsimonious.grammar import Grammar
from GroundProblogVisitor import GroundProblogVisitor


def file_to_string(filename):
    with open(filename) as input_file:
        return input_file.read()


class GroundProblogParser():
    def __init__(self):
        self._visitor = GroundProblogVisitor()

    def _grammar(self):
        # A PEG grammar for ground Problog. It is written in a very weird way
        # in order to make the visiting of the parse tree work.
        return Grammar(r"""
            program          = _ clauses
            clauses          = clause*
            clause           = predicate dot
            predicate        = prob_decls / rule / fact
            
            fact             = term _
            
            rule             = term turnstile rule_body
            rule_body        = conjunction / term
            conjunction      = term conjunction_opt
            conjunction_opt  = conjunction_more?
            conjunction_more = comma conjunction

            prob_decls       = prob_decl prob_decls_opt
            prob_decls_opt   = prob_decls_more?
            prob_decls_more  = semicolon prob_decls
            prob_decl        = probability doublecolon rule_predicate
            rule_predicate   = rule / fact
            
            term             = negation_opt word arguments_opt
            negation_opt     = negation?
            arguments_opt    = arguments?
            arguments        = lparen arguments_list rparen
            arguments_list   = term arguments_more_o
            arguments_more_o = arguments_more?
            arguments_more   = comma arguments_list
            
            probability      = decimal / fraction
            fraction         = number slash number
            word             = ~"[a-zA-Z0-9_]+"
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
        root_node = self._grammar().parse(program)
        print(root_node, '\n====================================================\n')
        return self._visitor.visit(root_node)


parser = GroundProblogParser()
program = file_to_string("files/test.grounded.pl")
parser.parse(program)
