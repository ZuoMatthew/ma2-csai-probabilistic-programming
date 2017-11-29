from BayesModel import BayesModel
from CNFEnc1 import CNFEnc1

def loadModel(file):
    return BayesModel(file)


def toEnc1(bayes):
    cnf = CNFEnc1(bayes)
    cnf.convert()
    return cnf


