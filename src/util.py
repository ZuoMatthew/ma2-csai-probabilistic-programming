def file_to_string(filename):
    with open(filename) as input_file:
        return input_file.read()


class IncrementingDict:
    def __init__(self):
        self.d = {}

    def get(self, element):
        if element in self.d:
            return self.d[element]
        else:
            num = len(self.d) + 1
            self.d[element] = num
            return num

    def items(self):
        return sorted(self.d.items(), key=lambda kv: kv[1])
