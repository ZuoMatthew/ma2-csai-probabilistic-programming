from wmc.SDD import SDD
from wmc.MiniC2D import MiniC2D


class WeightedModelCounter:
    """ Abstract class for weighted model counters. """

    def evaluate_cnf(self, cnf):
        """ Executes weighted model counting on a given weighted CNF. """
        raise NotImplementedError

    @staticmethod
    def factory(package):
        if package == "SDD":
            return SDD("")
        elif package == "MiniC2D":
            return MiniC2D("")
        else:
            raise Exception("Unknown model counter")
