def file_to_string(filename):
    with open(filename) as input_file:
        return input_file.read()