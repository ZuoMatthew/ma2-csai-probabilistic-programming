import sys
import os.path
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from BayesianNetwork import BayesianNetwork


parser = argparse.ArgumentParser(description='Arguments for bayes to encoding')
parser.add_argument("-f", "--file", dest="file", help="bayesian network file")
parser.add_argument("-o", "--output", dest="output", help="encoding output file")

parser.add_argument("-enc2", dest="enc2", action="store_true", default=False)
parser.add_argument("-c", "--cachet", dest="to_cachet", action="store_true", default=False)

if __name__ == '__main__':
    args = parser.parse_args()

    network = BayesianNetwork.create_from_file(args.file)

    if not args.enc2:
        enc1_cnf = network.to_enc1()
        enc1_cnf.convert()
        # enc1_cnf.elimEquiv()
        # print("converted enc1: \n", enc1_cnf.elimEquiv())
        enc1 = enc1_cnf.elimEquiv().toDimac(toCachet=args.to_cachet)
        # print("dimac:\n", enc1)
        f = open(f"{args.output}", "w")
        f.write(enc1)
        f.close()
    else:
        enc2_cnf = network.to_enc2()
        enc2_cnf.convert()
        # print("converted enc2: \n", enc2_cnf.elimEquiv())
        enc2 = enc2_cnf.elimEquiv().toDimac(toCachet=args.to_cachet)
        # print("dimac:\n",enc2)
        f = open(f"{args.output}", "w")
        f.write(enc2)
        f.close()
    #
    # files = ["alarm", "andes", "hailfinder", "water", "child"]
    # for file in files:
    #     print(file)
    #     filename = os.path.join(os.path.dirname(__file__), "..", "files", "networks", f"{file}.dsc")
    #     network = BayesianNetwork.create_from_file(filename)
    #
    #     toCachet_bools = [False, True]
    #     for toCachet in toCachet_bools:
    #         output_folder = "/home/thierry/Desktop/unif/capita/ma2-csai-probabilistic-programming/solutions/encodings/"
    #
    #         if toCachet:
    #             output_folder = output_folder + file + "/cachet"
    #         else:
    #             output_folder = output_folder + file + "/minic2d"
    #
    #         enc1_cnf = network.to_enc1()
    #         enc1_cnf.convert()
    #         #enc1_cnf.elimEquiv()
    #         #print("converted enc1: \n", enc1_cnf.elimEquiv())
    #         enc1 = enc1_cnf.elimEquiv().toDimac(toCachet=toCachet)
    #         #print("dimac:\n", enc1)
    #         f = open(f"{output_folder}/enc1.dimac", "w")
    #         f.write(enc1)
    #         f.close()
    #
    #         enc2_cnf = network.to_enc2()
    #         enc2_cnf.convert()
    #         #print("converted enc2: \n", enc2_cnf.elimEquiv())
    #         enc2 = enc2_cnf.elimEquiv().toDimac(toCachet=toCachet)
    #         #print("dimac:\n",enc2)
    #         f = open(f"{output_folder}/enc2.dimac", "w")
    #         f.write(enc2)
    #         f.close()
