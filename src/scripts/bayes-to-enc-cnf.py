import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from BayesianNetwork import BayesianNetwork

if __name__ == '__main__':
    files = ["alarm", "andes", "hailfinder", "water", "child"]
    for file in files:
        print(file)
        filename = os.path.join(os.path.dirname(__file__), "..", "files", "networks", f"{file}.dsc")
        network = BayesianNetwork.create_from_file(filename)

        toCachet_bools = [False, True]
        for toCachet in toCachet_bools:
            output_folder = "/Users/thierryderuyttere/Desktop/Unif_2e_master/capita_selecta/csai-probabilistic-programming/solutions/tests/"

            if toCachet:
                output_folder = output_folder + file + "/cachet"
            else:
                output_folder = output_folder + file + "/minic2d"

            enc1_cnf = network.to_enc1()
            enc1_cnf.convert()
            #print("converted enc1: \n", enc1_cnf.elimEquiv())
            enc1 = enc1_cnf.toDimac(toCachet=toCachet)
            #print("dimac:\n", enc1)
            f = open(f"{output_folder}/enc1.dimac", "w")
            f.write(enc1)
            f.close()

            enc2_cnf = network.to_enc2()
            enc2_cnf.convert()
            #print("converted enc2: \n", enc2_cnf.elimEquiv())
            enc2 = enc2_cnf.toDimac(toCachet=toCachet)
            #print("dimac:\n",enc2)
            f = open(f"{output_folder}/enc2.dimac", "w")
            f.write(enc2)
            f.close()
