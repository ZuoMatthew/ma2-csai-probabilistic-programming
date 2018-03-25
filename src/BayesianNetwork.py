# represents a node in the network
from enc.ENC1 import ENC1
from enc.ENC2 import ENC2


class Node:
    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.probabilities = None

    def __str__(self):
        return "[Node name: {}, values: {}, probabilities: {}]".format(self.name,self.values,self.probabilities)


# Is a single probability
class Probability:

    def __init__(self, forVal, prob, evidence=None):
        # forVal is something like True, False, 1, 0, so whenever our variable has value X then we have prob
        self.forVal = forVal
        self.prob = prob

        # Some probabilities have evidence
        self.evidence = evidence


# Is the full probability function for a node
class ProbabilityFunction:

    def __init__(self, probFor, dependents, probabilities):
        self.probFor = probFor

        # Refer to yourself
        self.probFor.probabilities = self

        # on what probabilities do you depend...
        self.dependents = dependents

        # what are the probabilities
        #self.probabilities = probabilities

        self.prob = {}
        self.initProbMap(probabilities)

    def initProbMap(self, probabilities):
        # print(probabilities)
        for prob in probabilities:

            if prob.evidence is not None:
                current = self.prob
                for i, obs in enumerate(prob.evidence):
                    obs_token = self.dependents[i].values[int(obs)]
                    if obs_token not in current:
                        current[obs_token] = {}
                        current = current[obs_token]
                    else:
                        current = current[obs_token]

                    if i == (len(prob.evidence) - 1):
                        current[self.probFor.values[int(prob.forVal)]] = prob.prob
            else:

                obs_token = self.probFor.values[int(prob.forVal)]
                self.prob[obs_token] = prob.prob

        print(self.prob)

    def get(self, kwargs):

        if len(kwargs) != len(self.dependents) + 1:
            print("Are you sure you passed the right amount of vars?")
            print("Passed: {}".format(kwargs))

        if len(self.dependents) == 0:
            #print(self.prob)
            #print(self.probFor)
            return self.prob[kwargs["value"]]

        else:
            current = self.prob
            for j in range(len(self.dependents)):
                current = current[kwargs[self.dependents[j].name]]

            return current[kwargs["value"]]


class BayesianNetwork:

    def __init__(self, nodes=None, probabilities=None):
        self.nodes = nodes if nodes is not None else {}
        self.probabilities = probabilities if probabilities is not None else {}

    def getProbabilityFunction(self, nodeName):
        # print(self.probabilities)
        return self.probabilities[nodeName]

    def getNodes(self):
        return self.nodes

    def to_enc1(self):
        return ENC1(self)

    def to_enc2(self):
        return ENC2(self)

    @staticmethod
    def create_from_file(filename):
        network = BayesianNetwork()

        f = open(filename, "r")
        lines = f.readlines()

        # Strip \n
        stripped = " ".join([line.strip("\n") for line in lines[1:]])

        # Split file on }
        splitted = network._splitLinesOnLastParenth(stripped)

        # Now we need to do pattern matching
        for split in splitted:
            temp = split.split(" ")
            while temp[0] == "":
                temp = temp[1:]

            if temp[0] == "node":
                name = temp[1]
                vals = network._getNodeInfo(temp[2:])
                #print("{} {}".format(name, vals))

                network.nodes[name] = Node(name, vals)

            elif temp[0] == "probability":
                # there is a '(' before
                probFor = network.nodes[temp[2]]
                dependant = []
                idx = 3

                if temp[idx] == "|":
                    # dependant on some probabilities
                    idx += 1
                    while temp[idx] != ")":
                        dependant.append(network.nodes[temp[idx].replace(",", "")])
                        idx += 1

                # Lets get the probabilities
                probabilities = network._getProbs(temp[(idx+1):])
                #print("{} {} {}".format(probFor, [str(d) for d in dependant], probabilities))
                network.probabilities[probFor.name] = ProbabilityFunction(probFor, dependant, probabilities)

        return network

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
            for j in range(len(prob)):
                probabilities.append(Probability(j, prob[j]))
            #probabilities.append(Probability(1, prob[1]))
        else:
            for recombined in temp_recombined_strings:
                split = recombined.split(":")
                obs = split[0].strip("()").split(",")
                prob = split[1].strip(";").split(",")

                for i in range(len(prob)):
                    probabilities.append(Probability(i, prob[i], obs))

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

