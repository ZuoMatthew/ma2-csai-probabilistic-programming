from wmc.MiniC2D import MiniC2D
from wmc.SDD import SDD


def create(package):
    if package == "SDD":
        return SDD("")
    elif package == "MiniC2D":
        return MiniC2D("")
    else:
        raise Exception("Unknown model counter")
