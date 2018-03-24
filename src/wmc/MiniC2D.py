import re
import os.path
import subprocess
from sys import platform
from wmc.WeightedModelCounter import WeightedModelCounter


class MiniC2D(WeightedModelCounter):
    """ WMC using the miniC2D package, which does knowledge compilation and model counting based on exhaustive DPLL. """

    def __init__(self, options):
        dir_platform = "darwin" if platform == "darwin" else "linux"
        self.counter_path = os.path.join(os.path.dirname(__file__), "..", "..", "model_counters",
                                         "miniC2D-1.0.0", "bin", dir_platform, "miniC2D")

        if not os.path.exists(self.counter_path):
            raise Exception("Could not find miniC2D installation. Expected location: {}".format(self.counter_path))

        self.options = options

    def create_vtree(self, filename):
        dir = os.path.abspath(os.path.dirname(filename))

        cnf_params = "--cnf {}".format(os.path.abspath(filename))
        vtree_params = "--vtree_method 0 --vtree_out {dir}/vtree.txt --vtree_dot {dir}/vtree.dot".format(dir=dir)
        command = "{} {} {} {}".format(self.counter_path, cnf_params, vtree_params, self.options)

        completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        return "{dir}/vtree.txt".format(dir=dir)

    def do_model_count(self, filename):
        filename = os.path.abspath(filename)
        dir = os.path.dirname(filename)
        vtree_f = os.path.join(dir, "vtree.")

        cnf_params = "--model_counter --cnf {}".format(filename)
        vtree_params = "--vtree_method 0 --vtree_out {} --vtree_dot {}".format(vtree_f + "txt", vtree_f + "dot")
        command = "{} {} {} {}".format(self.counter_path, cnf_params, vtree_params, self.options)

        completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = completed_process.stdout.decode()

        # convert the new vtree.dot file to a png file
        subprocess.check_call(["dot", "-Tpng", vtree_f + "dot", "-o", vtree_f + "png"])
        match = re.search(r"Count(/Probability)?\s\t(.*)", output)

        if match is None:
            return None
        return match.group(2)
