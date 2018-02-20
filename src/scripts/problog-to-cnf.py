import GroundProblogParser
import util

parser = GroundProblogParser.GroundProblogParser()
program = util.file_to_string("../files/test.grounded.pl")
cnf = parser.parse_to_CNF(program)
