from problog.program import PrologFile
from problog.tasks.sample import sample
import os
here = os.path.dirname(os.path.realpath(__file__))

pl = PrologFile(here + "/../files/problog/alarm.pl")
for imp in sample(pl,n=10):
    print(imp)
    print("="*8)