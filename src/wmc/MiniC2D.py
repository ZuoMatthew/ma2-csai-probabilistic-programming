import os.path
from wmc.WeightedModelCounter import WeightedModelCounter


class MiniC2D(WeightedModelCounter):
    """ WMC using the miniC2D package, which does knowledge compilation and model counting based on exhaustive DPLL. """

    def __init__(self, options):
        self.counter_path = os.path.abspath("../../model_counters/miniC2D-1.0.0/bin/linux/miniC2D")
        self.options = options
        pass

    def do_model_count(self, filename):
        dir = os.path.abspath(os.path.dirname(filename))
        print("Will save vtree files in dir:", dir)

        cnf_params = "--model_counter --cnf {}".format(filename)
        vtree_params = "--vtree_method 0 --vtree_out {dir}/vtree.txt --vtree_dot {dir}/vtree.dot".format(dir=dir)
        command = "{} {} {} {}".format(self.counter_path, cnf_params, vtree_params, self.options)

        return "TODO: MiniC2D probability result"
