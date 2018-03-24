import os.path
from wmc import factory as CounterFactory
from wmc.WeightedModelCounter import WeightedModelCounter
from pysdd.sdd import SddManager, Vtree, WmcManager


class SDD(WeightedModelCounter):
    """ WMC using the SDD package, which allows users to construct, manipulate, and optimize SDDs. """

    def __init__(self):
        pass

    def get_weights_from_cnf(self, filename):
        cnf = open(os.path.abspath(filename), "r")
        lines = cnf.readlines()
        weights = []
        for line in lines:
            if "weight" in line:
                splitted = line.strip("\n").split(" ")
                weights = splitted[2:-1]
                # print(weights)
                weights = [float(w) for w in weights]

        return weights

    # Based on http://pysdd.readthedocs.io/en/latest/examples/model_counting.html
    def do_model_count(self, filename):
        print(filename)
        # 1. create VTREE
        vtree_path = CounterFactory.create("minic2d").create_vtree(filename)
        vtree = Vtree.from_file(bytes(vtree_path.encode('utf-8')))

        sdd = SddManager.from_vtree(vtree)

        # print(filename)
        # 2. read CNF
        root = sdd.read_cnf_file(bytes(os.path.abspath(filename).encode('utf-8')))

        # model counting
        wmc = root.wmc(log_mode=False)

        # Add weights
        lits = [sdd.literal(i) for i in range(1, sdd.var_count() + 1)]
        weights = self.get_weights_from_cnf(filename)

        for i in range(len(lits)):
            wmc.set_literal_weight(lits[i], weights[2 * i])
            wmc.set_literal_weight(-lits[i], weights[2 * i + 1])

        w = wmc.propagate()
        return w
