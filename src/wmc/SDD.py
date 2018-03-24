import re
import os.path
import subprocess
from sys import platform
from wmc.WeightedModelCounter import WeightedModelCounter
from lib.PySDD.pysdd.sdd import SddManager, Vtree, WmcManager
from wmc.MiniC2D import MiniC2D

class SDD(WeightedModelCounter):
    """ WMC using the SDD package, which allows users to construct, manipulate, and optimize SDDs. """

    def __init__(self):
        pass

    # Based on http://pysdd.readthedocs.io/en/latest/examples/model_counting.html
    def do_model_count(self, filename):
        # 1. create VTREE
        vtree_path = MiniC2D("").create_vtree(filename)
        vtree = Vtree.from_file(bytes(vtree_path.encode('utf-8')))

        sdd = SddManager.from_vtree(vtree)

        #print(filename)
        # 2. read CNF
        root = sdd.read_cnf_file(bytes(os.path.abspath(filename).encode('utf-8')))

        # Weighted model counting
        wmc = root.wmc(log_mode=True)
        w = wmc.propagate()


        return w
