import util

if __name__ == '__main__':
    filename = "../files/test.pl"
    program = util.file_to_string(filename)

    util.evaluate_using_problog(program, print_steps=True)
