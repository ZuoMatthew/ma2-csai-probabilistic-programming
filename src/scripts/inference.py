import sys
import os.path
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import util as util

parser = argparse.ArgumentParser(description='Arguments for inference')
parser.add_argument('--problog_file', dest="pf", default=None, help="A problog file")
parser.add_argument("--model_counter", dest="model_counter", help="The model counter to use [minic2d, sdd]", default="sdd")
parser.add_argument("--bayesian_network", dest="bn", default=None, help="A bayesian network file")

if __name__ == '__main__':
    args = parser.parse_args()
    if args.pf is None and args.bn is None:
        parser.error("Please provide a problog file (--problog_file) or a bayesian network (--bayesian_network)")

    filename = args.pf if args.pf is not None else args.bn
    is_network = True if args.bn else False
    model_counter = None
    if args.model_counter.lower() == "sdd":
        model_counter = "sdd"
    elif args.model_counter.lower() == "minic2d":
        model_counter = "minic2d"
    else:
        print('Given model counter not supported (sdd, minic2d).')
        sys.exit(1)

    ground_program = util.load_problog_or_network_as_ground_problog(filename, is_network)
    results = util.results_with_pipeline(ground_program, counter=args.model_counter, print_steps=True)
    problog_results = util.results_with_problog(ground_program, print_steps=False)

    print(util.separator_1)
    print("EVALUATION USING PROBLOG LIBRARY:")
    query_str_len = max([len(q) for q, _ in problog_results]) if problog_results else None
    for query, probability in problog_results:
        print("{:<{}}: {}".format(query, query_str_len, probability))

