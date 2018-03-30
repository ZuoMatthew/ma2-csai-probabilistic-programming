import sys
import os.path
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import util as util

parser = argparse.ArgumentParser(description='Arguments for inference')
parser.add_argument('--problog_file', dest="pf", default=None, help="A problog file we want to parse")
parser.add_argument("--counter", dest="counter", help="Which counter we want to use [minic2d, sdd]", default="minic2d")
parser.add_argument("--bayesian_network", dest="bn", default=None, help="A bayesian network file")

if __name__ == '__main__':
    args = parser.parse_args()
    if args.pf is None and args.bn is None:
        parser.error("Please provide a problog file (with --problog_file) or a bayesian network (with --bayesian_network)")

    file = args.pf if args.pf is not None else args.bn
    is_network = True if args.bn else False

    results = util.results_with_pipeline(file, counter=args.counter, print_steps=True)
    problog_results = util.results_with_problog(file, print_steps=False)

    print(util.separator_1)
    print("EVALUATION USING PROBLOG LIBRARY:")
    query_str_len = max([len(q) for q, _ in problog_results]) if problog_results else None
    for query, probability in problog_results:
        print("{:<{}}: {}".format(query, query_str_len, probability))

