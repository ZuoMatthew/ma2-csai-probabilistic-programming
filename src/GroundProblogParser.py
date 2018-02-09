"""
A parser for ground ProbLog programs.
"""

from parsimonious.grammar import Grammar


def file_to_string(filename):
    with open(filename) as input_file:
        return input_file.read()


class GroundProblogParser():
    def _grammar(self):
        # statement, term, atom, conjunction, disjunction, rule
        return Grammar(r"""
            program       = ~"\n*" clause*
            clause        = comment / fact / rule
            
            comment       = "%" line ~"\n*"
            
            fact          = term end_clause
            
            rule          = term ~" *:- *" predicate* end_clause
            predicate     = conjunction / disjunction
            conjunction   = (term ~" *, *" conjunction) / term
            disjunction   = (term ~" *; *" disjunction) / term
            
            compound_term = word
            term          = (functor "(" arguments ")") / functor
            functor       = word
            arguments     = (word "," arguments) / word
            
            line          = ~"[a-zA-Z0-9_ ]*"
            word          = ~"[a-zA-Z0-9_]+"
            end_clause    = ~" *\. *\n*"
            number        = ~"[0-9]*"
            variable      = ~"[A-Z _]"
            newline       = ~"\s"
        """)

    def parse(self, program):
        return self._grammar().parse(program)


parser = GroundProblogParser()
program = file_to_string("files/test.grounded.pl")
print(parser.parse(program))
