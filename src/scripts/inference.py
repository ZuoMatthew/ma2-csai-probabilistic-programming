import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import util as util

if __name__ == '__main__':
    file = "test.pl"
    results = util.results_with_pipeline(file, print_steps=FileExistsError)
    problog_results = util.results_with_problog(file, print_steps=False)

    print(util.separator_1)
    print("EVALUATION USING PROBLOG LIBRARY:")
    query_str_len = max([len(q) for q, _ in problog_results]) if problog_results else None
    for query, probability in problog_results:
        print("{:<{}}: {}".format(query, query_str_len, probability))
