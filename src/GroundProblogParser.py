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
            program     = newlines clause*
            clause      = (comment newlines) / ((prob_decls / rule / fact) end_clause)
            
            fact        = term
            
            rule        = term turnstile (conjunction / disjunction / term)
            # which conjunction to use? see later when defining visitor that will build the CNF
            #conjunction = term (comma conjunction)?
            #conjunction = (term comma conjunction) / term
            conjunction = term (comma term)*
            disjunction = (term semicolon disjunction) / term

            prob_decls  = prob_decl (semicolon prob_decls)?
            prob_decl   = probability doublecolon (rule / fact)
            
            term        = negation? functor ("(" arguments ")")?
            functor     = word
            arguments   = (term comma arguments) / term
            
            newlines    = ~"\n*"
            comment     = ~"%.*"
            word        = ~"[a-zA-Z0-9_]+"
            end_clause  = ~" *\. *\n*"
            number      = ~"[0-9]*"
            variable    = ~"[A-Z_][a-zA-Z0-9_]*"
            negation    = ~" *" "\+" ~" *"
            comma       = ~" *, *"
            semicolon   = ~" *; *"
            doublecolon = ~" *:: *"
            turnstile   = ~" *:- *"
            probability = decimal / fraction
            decimal     = ~"[0-9]*\.[0-9]*"
            fraction    = (number "/" number)
        """)

    def parse(self, program):
        return self._grammar().parse(program)


parser = GroundProblogParser()
program = file_to_string("files/test.grounded.pl")
print(parser.parse(program))
