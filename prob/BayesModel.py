class Node:

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.probabilities = None

    def __str__(self):
        return "[Node name: {}, values: {}, probabilities: {}]".format(self.name,self.values,self.probabilities)

class Probability:
    def __init__(self, forVal, prob, observation=None):
        self.forVal = forVal
        self.prob = prob
        self.observation = observation

class ProbabilityFunction:

    def __init__(self, probFor, dependents, probabilities):
        self.probFor = probFor

        # Refer to yourself
        self.probFor.probabilities = self

        # on what probabilities do you depend...
        self.dependents = dependents

        # what are the probabilities
        self.probabilities = probabilities

        self.prob = {}
        self.initProbMap(probabilities)


    def initProbMap(self, probabilities):

        print(probabilities)
        for prob in probabilities:

            if prob.observation is not None:
                current = self.prob
                for i, obs in enumerate(prob.observation):
                    obs_token = self.dependents[i].values[int(obs)]
                    if obs_token not in current:
                        current[obs_token] = {}
                        current = current[obs_token]
                    else:
                        current = current[obs_token]

                    if i == len(prob.observation) - 1:
                        current[self.probFor.values[int(prob.forVal)]] = prob.prob
            else:

                obs_token = self.probFor.values[int(prob.forVal)]
                self.prob[obs_token] = prob.prob

        print(self.prob)

class BayesModel:

    def __init__(self, file):
        self.nodes = {}
        self.probabilities = {}
        self._loadFromFile(file)
        pass

    def _loadFromFile(self, file):
        f = open(file, "r")
        lines = f.readlines()

        # Strip \n
        stripped = " ".join([line.strip("\n") for line in lines[1:]])

        # Split file on }
        splitted = self._splitLinesOnLastParenth(stripped)

        # Now we need to do pattern matching
        for split in splitted:
            temp = split.split(" ")
            while temp[0] == "":
                temp = temp[1:]

            if temp[0] == "node":
                name = temp[1]
                vals = self._getNodeInfo(temp[2:])
                #print("{} {}".format(name, vals))
                self.nodes[name] = Node(name, vals)

            elif temp[0] == "probability":
                # there is a '(' before
                probFor = self.nodes[temp[2]]
                dependant = []
                idx = 3

                if temp[idx] == "|":
                    # dependant on some probabilities
                    idx += 1
                    while temp[idx] != ")":
                        dependant.append(self.nodes[temp[idx].replace(",", "")])
                        idx += 1

                # Lets get the probabilities
                probabilities = self._getProbs(temp[(idx+1):])
                #print("{} {} {}".format(probFor, [str(d) for d in dependant], probabilities))
                self.probabilities[probFor] = ProbabilityFunction(probFor, dependant, probabilities)


    def _getProbs(self,probs):
        temp_recombined_strings = []
        str = ""
        probabilities = []
        for p in probs:

            if p != "" and p != "{" and p != "}":
                str += p
                if ";" in p:
                    temp_recombined_strings.append(str)
                    str = ""

        if str != "":
            temp_recombined_strings.append(str)

        if len(temp_recombined_strings) == 1:
            # Only 1 entry so we can just ge it out
            prob = temp_recombined_strings[0].strip(";").split(",")
            probabilities.append(Probability(0, prob[0]))
            probabilities.append(Probability(1, prob[1]))
        else:
            for recombined in temp_recombined_strings:
                split = recombined.split(":")
                obs = split[0].strip("()").split(",")
                prob = split[1].strip(";").split(",")

                probabilities.append(Probability(0, prob[0], obs))
                probabilities.append(Probability(1, prob[1], obs))

        return probabilities

    def _getNodeInfo(self, nodeSplit):
        num_vals = 0
        values = []
        index = 0
        while index < len(nodeSplit):

            while not nodeSplit[index].isdigit():
                index += 1
                if index >= len(nodeSplit):
                    return values

            if nodeSplit[index].isdigit():
                num_vals = int(nodeSplit[index])
                while nodeSplit[index] != "{":
                    index += 1
                index += 1

                for j in range(num_vals):
                    values.append(nodeSplit[index+j].replace(",", "").replace("\"", ""))

                return values
            index += 1

        return values


    def _splitLinesOnLastParenth(self, lines):
        splitted = []
        str = ""
        stack = 0
        for c in lines:
            str += c

            if c == "{":
                stack += 1
            elif c == "}":
                stack -= 1
                if stack == 0:
                    splitted.append(str)
                    str = ""

        return splitted

