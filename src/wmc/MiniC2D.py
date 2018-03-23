from wmc.WeightedModelCounter import WeightedModelCounter


class MiniC2D(WeightedModelCounter):
    """ WMC using the miniC2D package, which does knowledge compilation and model counting based on exhaustive DPLL. """

    def __init__(self, options):
        pass

    def do_model_count(self, cnf):
        return "TODO: MiniC2D probability result"
