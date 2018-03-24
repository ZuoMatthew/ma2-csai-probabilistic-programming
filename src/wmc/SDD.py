import re
import os.path
import subprocess
from sys import platform
from wmc.WeightedModelCounter import WeightedModelCounter
from lib.PySDD.pysdd.sdd import SddManager, Vtree, WmcManager
from wmc.MiniC2D import MiniC2D
class SDD(WeightedModelCounter):
    """ WMC using the SDD package, which allows users to construct, manipulate, and optimize SDDs. """

    def __init__(self, options):
        bin_platform = "darwin" if platform == "darwin" else "linux"
        self.counter_path = os.path.join(os.path.dirname(__file__), "..", "..", "model_counters",
                                         "sdd-2.0", "bin", "sdd-{}".format(bin_platform))

        if not os.path.exists(self.counter_path):
            raise Exception("Could not find SDD installation. Expected location: {}".format(self.counter_path))

        self.options = options

    # Based on http://pysdd.readthedocs.io/en/latest/examples/model_counting.html
    def do_model_count(self, filename):
        # 1. create VTREE
        vtree = Vtree.from_file(MiniC2D("").create_vtree(filename))

        sdd = SddManager.from_vtree(vtree)

        # 2. read CNF
        root = sdd.read_cnf_file(os.path.abspath(filename))

        # Weighted model counting
        wmc = root.wmc(log_mode=True)

        w = wmc.propagate()

        return w
