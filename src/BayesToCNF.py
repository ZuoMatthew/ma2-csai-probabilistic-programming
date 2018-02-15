from BayesModel import BayesModel
from CNFEnc1 import CNFEnc1
from CNFEnc2 import CNFEnc2

def loadModel(file):
    return BayesModel(file)

def toEnc1(bayes):
    cnf = CNFEnc1(bayes)
    cnf.convert()
    return cnf

def toEnc2(bayes):
    cnf = CNFEnc2(bayes)
    cnf.convert()
    return cnf

enc = toEnc1(loadModel("files/cancer.dsc"))
#print("enc: \n", enc)
print("converted enc: \n", enc.elimEquiv())
print("dimac:\n", enc.toWeightedDimac())