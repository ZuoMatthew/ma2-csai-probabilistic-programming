class Variable:

    def __init__(self, var, value, negate=False):
        self.var = var
        self.value = value
        self.negate = negate


    def __str__(self):
        base = self.var[0] + "_" + self.value
        if self.negate:
            return """~\lambda_{}""".format(base)

        return """\lambda_{}""".format(base)

    def toLATEX(self):
        return str(self)


class Weight:

    def __init__(self, lhs, prob):
        self.lhs = lhs
        self.prob = prob

    def __str__(self):
        return """W({}) = {}""".format(self.lhs, self.prob)



class Conditional:

    def __init__(self, var):
        self.var = var

    def __str__(self):
        base = self.var.var[0] + "_" + self.var.value
        return """{}""".format(base)

    def asVar(self):
        return self.var

    def toLATEX(self):
        return str(self)


class CPT:

    def __init__(self, var, value, conditional, token="\\theta", negate=False):
        self.var = var
        self.value = value
        self.conditional = conditional
        self.token = token
        self.negate = negate

    def __str__(self):
        if len(self.conditional) > 0:
            base = self.var.var[0] + "_" + self.var.value + "|" + " ".join([c.toLATEX() for c in self.conditional])
        else:
            base = self.var.var[0] + "_" + self.var.value
        if self.negate:
            return """~{}_{}""".format(self.token, base)

        return """{}_{}""".format(self.token, base)

    def toLATEX(self):
        return str(self)


class IndicatorClause:

    def __init__(self, vars):
        self.vars = vars

    def __str__(self):
        return " v ".join([str(v) for v in self.vars])

    def toLATEX(self):
        return str(self)

class ParameterClause:
    def __init__(self,lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    # Gets the clause as
    # a => b
    # instead of a <=> b
    def simplified(self):
        ret = []
        conj = "^".join([str(l) for l in self.lhs])
        ret.append(conj + " => " + str(self.rhs))

        for l in self.lhs:
            ret.append(str(self.rhs) + " => " + str(l))

        return ret


    def __str__(self):
        conj = " ∧ ".join([str(l) for l in self.lhs])
        return """{} <=> {}""".format(conj, self.rhs)

class CNF:

    def __init__(self, bayes):
        self.vars = {}
        self.CPT = []
        self.bayes = bayes
        self.indicators = []
        self.paramClauses = []
        self.weights = []