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
        # statement, term, atom, conjunction, disjunction, rule
        return Grammar(r"""
            program     = _ clauses
            clauses     = clause*
            clause      = comment / predicate
            predicate   = prob_decls / rule / fact
            
            fact        = term end_clause
            
            rule        = term turnstile (conjunction / disjunction / term) end_clause
            # which conjunction to use? see later when defining visitor that will build the CNF
            #conjunction = term (comma conjunction)?
            #conjunction = (term comma conjunction) / term
            conjunction = term (comma term)*
            disjunction = (term semicolon disjunction) / term

            prob_decls  = prob_decl (semicolon prob_decls)? end_clause
            prob_decl   = probability doublecolon (rule / fact)
            
            term        = negation_opt word arguments_opt
            arguments_opt = lparen arguments rparen
            arguments   = (term comma arguments) / term
            
            comment     = ~r"%[^\r\n]*" _
            word        = ~"[a-zA-Z0-9_]+"
            end_clause  = _ "." _
            number      = ~"[0-9]*"
            variable    = ~"[A-Z_][a-zA-Z0-9_]*"
            negation_opt = (_ "\+" _)?
            comma       = _ "," _
            semicolon   = _ ";" _
            doublecolon = _ "::" _
            turnstile   = _ ":-" _
            lparen      = _ "(" _
            rparen      = _ ")" _
            probability = decimal / fraction
            decimal     = ~"[0-9]*\.[0-9]*"
            fraction    = (number "/" number)

            _ = meaninglessness*
            meaninglessness = ~r"\s+"
        """)

    def parse(self, program):
        root_node = self._grammar().parse(program)
        print(root_node, '\n====================================================\n')
        return self._visitor.visit(root_node)


parser = GroundProblogParser()
program = file_to_string("files/test.grounded.pl")
parser.parse(program)
