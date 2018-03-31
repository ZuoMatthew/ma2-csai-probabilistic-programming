from problog.program import PrologFile, PrologString
from problog.tasks.sample import sample
from problog.learning.lfi import extract_evidence
import os
here = os.path.dirname(os.path.realpath(__file__))

pl = PrologFile(here + "/../files/problog/cancer.pl")

for imp in sample(pl,n=10, as_evidence=True):
    print(imp)
    print("="*8)