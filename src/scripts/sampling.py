from problog.program import PrologFile, PrologString

from problog.engine import DefaultEngine
from problog.logic import Term
from problog.tasks.sample import sample
from problog.learning.lfi import extract_evidence
import os
here = os.path.dirname(os.path.realpath(__file__))

pl = PrologFile(here + "/../files/problog/test.pl")

for imp in sample(pl,n=10, as_evidence=True):
    engine = DefaultEngine()
    atoms = engine.query(pl, Term('evidence', None, None))
    atoms1 = engine.query(pl, Term('evidence', None))
    print(imp)
    print("="*8)