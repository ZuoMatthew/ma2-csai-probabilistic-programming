import util
from InferenceEngine import InferenceEngine


if __name__ == '__main__':
    filename = "../files/test.grounded.pl"
    program = util.file_to_string(filename)

    engine = InferenceEngine()
    engine.evaluate_problog_program(program)
