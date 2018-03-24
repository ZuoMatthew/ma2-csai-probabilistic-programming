import os.path
from wmc.WeightedModelCounter import WeightedModelCounter
from lib.PySDD.pysdd.sdd import SddManager, Vtree, WmcManager

class SDD(WeightedModelCounter):
    """ WMC using the SDD package, which allows users to construct, manipulate, and optimize SDDs. """

    def __init__(self):
        pass

    # Based on http://pysdd.readthedocs.io/en/latest/examples/model_counting.html
    def do_model_count(self, filename):
        # 1. create VTREE
        vtree = Vtree.from_file("FILE.vtree")

        sdd = SddManager.from_vtree(vtree)

        # 2. read CNF
        root = sdd.read_cnf_file(os.path.abspath(filename))

        wmc = root.wmc(log_mode=True)
        w = wmc.propagate()

        return w
