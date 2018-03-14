from BayesianNetwork import BayesianNetwork

if __name__ == '__main__':
    filename = "files/abc.dsc"
    network = BayesianNetwork.create_from_file(filename)

    enc1_cnf = network.to_enc1()
    enc1_cnf.convert()
    print("converted enc1: \n", enc1_cnf.elimEquiv())
    print("dimac:\n", enc1_cnf.toDimac(toCachet=False))

    enc2_cnf = network.to_enc2()
    enc2_cnf.convert()
    print("converted enc2: \n", enc2_cnf.elimEquiv())
    print("dimac:\n", enc2_cnf.toDimac(toCachet=False))
