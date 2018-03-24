import re
import os.path
import subprocess
from sys import platform
from wmc.WeightedModelCounter import WeightedModelCounter


class SDD(WeightedModelCounter):
    """ WMC using the SDD package, which allows users to construct, manipulate, and optimize SDDs. """

    def __init__(self, options):
        bin_platform = "darwin" if platform == "darwin" else "linux"
        self.counter_path = os.path.join(os.path.dirname(__file__), "..", "..", "model_counters",
                                         "sdd-2.0", "bin", "sdd-{}".format(bin_platform))

        if not os.path.exists(self.counter_path):
            raise Exception("Could not find SDD installation. Expected location: {}".format(self.counter_path))

        self.options = options

    def do_model_count(self, filename):
        return "TODO: SDD probability result"
