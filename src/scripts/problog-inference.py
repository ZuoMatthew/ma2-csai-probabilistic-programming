import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import util

if __name__ == '__main__':
    filename = os.path.join(os.path.dirname(__file__), "..", "files", "problog", "test.pl")
    program = util.file_to_string(filename)

    util.evaluate_using_problog_library(program, print_steps=True)
