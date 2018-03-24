import re
import os.path
import subprocess
from wmc.WeightedModelCounter import WeightedModelCounter
from sys import platform

class MiniC2D(WeightedModelCounter):
    """ WMC using the miniC2D package, which does knowledge compilation and model counting based on exhaustive DPLL. """

    def __init__(self, options):
        if platform == "linux" or platform == "linux2":
            self.counter_path = os.path.abspath("../../model_counters/miniC2D-1.0.0/bin/linux/miniC2D")
        elif platform == "darwin":
            self.counter_path = os.path.abspath("../../model_counters/miniC2D-1.0.0/bin/darwin/miniC2D")
        if not os.path.exists(self.counter_path):
            raise Exception("Could not find miniC2D installation. Expected location: {}".format(self.counter_path))
        self.options = options
        pass

    def do_model_count(self, filename):
        dir = os.path.abspath(os.path.dirname(filename))
        print("Will save vtree files in dir:", dir)

        cnf_params = "--model_counter --cnf {}".format(os.path.abspath(filename))
        vtree_params = "--vtree_method 0 --vtree_out {dir}/vtree.txt --vtree_dot {dir}/vtree.dot".format(dir=dir)
        command = "{} {} {} {}".format(self.counter_path, cnf_params, vtree_params, self.options)

        completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = completed_process.stdout.decode()

        # convert the new vtree.dot file to a png file
        subprocess.check_call(["dot", "-Tpng", dir+"/vtree.dot", "-o", dir+"/vtree.png"])

        match = re.search(r"Count\s\t(.*)", output)
        if match is None:
            return None
        return match.group(1)
