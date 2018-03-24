import os.path
from wmc.WeightedModelCounter import WeightedModelCounter


class SDD(WeightedModelCounter):
    """ WMC using the SDD package, which allows users to construct, manipulate, and optimize SDDs. """

    def __init__(self, options):
        self.counter_path = os.path.abspath("../../model_counters/sdd-2.0/bin/sdd-linux")
        if not os.path.exists(self.counter_path):
            raise Exception("Could not find SDD installation. Expected location: {}".format(self.counter_path))
        self.options = options
        pass

    def do_model_count(self, filename):
        return "TODO: SDD probability result"
