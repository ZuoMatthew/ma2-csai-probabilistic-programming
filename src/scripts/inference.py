import sys
import os.path
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import util as util

parser = argparse.ArgumentParser(description='Arguments for inference')
parser.add_argument("-p", "--problog", dest="problog", help="Evaluate a ProbLog file")
parser.add_argument("-pl", "--problog_learn", dest="problog_learn", help="Parameter learning on a ground ProbLog file with tunable probabilities")
parser.add_argument("-plt", "--problog_learn_truth", dest="problog_learn_truth", help="Ground ProbLog file with values probabilities to sample from for parameter learning")
parser.add_argument("-li", "--learning_interpretations", dest="learning_interpretations", default=10, help="Amount of interpretations to generate for parameter learning")
parser.add_argument("-mc", "--model_counter", dest="model_counter", help="The model counter to use [minic2d, sdd]", default="minic2d")
parser.add_argument("-bn", "--bayesian_network", dest="bn", help="A bayesian network file")

if __name__ == '__main__':
    args = parser.parse_args()

    if args.problog and args.problog_learn:
        parser.error("Please only choose one of --problog or --problog_learn")

    if args.problog:
        filename = args.problog
    elif args.problog_learn:
        filename = args.problog_learn
    elif args.bn:
        filename = args.bn
    else:
        parser.error("Please provide a problog file (--problog --problog_learn) or a bayesian network (--bn)")
        sys.exit(1)

    if args.model_counter.lower() == "minic2d":
        model_counter = "minic2d"
    elif args.model_counter.lower() == "sdd":
        model_counter = "sdd"
    else:
        parser.error("Given model counter not supported (sdd, minic2d).")
        sys.exit(1)

    parameter_learning = args.problog_learn is not None
    is_network = args.bn is not None

    if not parameter_learning:
        ground_program = util.load_problog_or_network_as_ground_problog(filename, is_network)

        results = util.results_with_pipeline(ground_program, model_counter, parameter_learning, print_steps=True)
        problog_results = util.results_with_problog(ground_program, print_steps=False)

        print(util.separator_1)
        print("EVALUATION USING PROBLOG LIBRARY:")
        query_str_len = max([len(q) for q, _ in problog_results]) if problog_results else None
        for query, probability in problog_results:
            print("{:<{}}: {}".format(query, query_str_len, probability))

    else:
        if args.problog_learn_truth is None:
            parser.error("Please provide a problog file with ground truth for probabilities filled in for generation of interpretations (--problog_learn_truth).")
            sys.exit(1)

        # if parameter learning, the program expects an already grounded file,
        # as grounding a file without queries would result in an empty program
        ground_program = util.file_to_string(filename)

        ground_truth_filename = args.problog_learn_truth
        amount_of_interpretations = int(args.learning_interpretations)
        interpretations = util.generate_interpretations(ground_truth_filename, amount_of_interpretations)

        util.results_with_pipeline(ground_program, model_counter, parameter_learning, interpretations, print_steps=True)
