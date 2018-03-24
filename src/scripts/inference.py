import util
import os.path
from InferenceEngine import InferenceEngine

if __name__ == '__main__':
    filename = os.path.join(os.path.dirname(__file__), "..", "files", "test.pl")
    program = util.file_to_string(filename)

    engine = InferenceEngine()
    engine.evaluate_problog_program(program)

    problog_results = util.evaluate_using_problog(program, print_steps=False)

    print(util.separator_1)
    print("EVALUATION USING PROBLOG LIBRARY:")
    query_str_len = max([len(q) for q, _ in problog_results])
    for query, probability in problog_results:
        print("{:<{}}: {}".format(query, query_str_len, probability))
