import re
import pydot
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
        self.vtree_params = "--vtree_method 0 --vtree_out {} --vtree_dot {}"

    def create_vtree(self, filename):
        filename = os.path.abspath(filename)
        dir = os.path.dirname(filename)
        vtree_f = os.path.join(dir, "vtree-minic2d.")

        cnf_params = "--cnf {}".format(filename)
        vtree_params = self.vtree_params.format(vtree_f + "txt", vtree_f + "dot")
        command = "{} {} {} {}".format(self.counter_path, cnf_params, vtree_params, self.options)

        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return vtree_f + "txt"

    def get_stats_from_output(self, output):
        pass

    
    def do_model_count(self, filename):
        filename = os.path.abspath(filename)
        dir = os.path.dirname(filename)
        vtree_file = os.path.join(dir, "vtree-minic2d.")

        cnf_params = "--model_counter --cnf {}".format(filename)
        # also need to run once without --model_counter to generate NNF stats (= SDD nodes and edges)
        nnf_params = "--cnf {}".format(filename)
        vtree_params = self.vtree_params.format(vtree_file + "txt", vtree_file + "dot")
        command = "{} {} {} {}".format(self.counter_path, cnf_params, vtree_params, self.options)

        completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = completed_process.stdout.decode()
        print(output)

        # convert the new vtree.dot file to a png file
        # (graph,) = pydot.graph_from_dot_file(vtree_file + "dot")
        # graph.write_png(vtree_file + "png")

        # get the model count from the output
        match = re.search(r"Count(/Probability)?\s\t(.*)", output)
        if match is None:
            return None, {}

        result = float(match.group(2))
        stats = self.get_stats_from_output(output)

        stats = {
            "Number of variables in the CNF": "CNF stats: vars",
            "Number of lines in the CNF": "CNF stats: clauses",
            "Statistics on the depth of the vtree": "???? vtree widths? vtree-minic2d.txt file bekijken?",
            "Number of edges in the circuit": "NNF stats: nnf nodes",
            "Number of nodes in the circuit": "NNF stats: nnf edges"
        }

        return result, stats
