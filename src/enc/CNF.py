import copy

class Variable:

    def __init__(self, var, value, negate=False):
        self.var = var
        self.value = value
        self.negate = negate

    def getBaseRepr(self):
        base = self.var + "_" + self.value
        return """\lambda_{}""".format(base)

    def __str__(self):
        base = self.getBaseRepr()
        if self.negate:
            return """~{}""".format(base)

        return base

    def toggleNegate(self):
        self.negate = not self.negate

    def getCopy(self, negate=False):
        c = copy.deepcopy(self)
        if negate:
            c.toggleNegate()
        return c

    def toLATEX(self):
        return str(self)


class Weight:

    def __init__(self, lhs, prob):
        self.lhs = lhs
        self.prob = prob

    def __str__(self):
        return """W({}) = {:.2f}""".format(self.lhs, float(self.prob))



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

    def toggleNegate(self):
        self.negate = not self.negate


    def getBaseRepr(self):
        if len(self.conditional) > 0:
            base = self.var.var[0] + "_" + self.var.value + "|" + " ".join([c.toLATEX() for c in self.conditional])
        else:
            base = self.var.var[0] + "_" + self.var.value

        return """{}_{}""".format(self.token, base)

    def __str__(self):
        base = self.getBaseRepr()
        if self.negate:
            return """~{}""".format(base)

        return base

    def getCopy(self, negate=False):
        c = copy.deepcopy(self)
        if negate:
            c.toggleNegate()
        return c

    def toLATEX(self):
        return str(self)


class IndicatorClause:

    def __init__(self, vars):
        self.vars = vars

    def __str__(self):
        return " v ".join([str(v) for v in self.vars])

    def toLATEX(self):
        return str(self)

class RemovedEquivClause:

    def __init__(self, P, Q, negateP):
        self.P = P
        self.Q = Q
        self.negateP = negateP
        self.negateQ = not negateP
        self.applyNegation()

    def applyNegation(self):
        if self.negateP:
            copied = []
            for v in self.P:
                copied.append(v.getCopy(negate=True))
            self.P = copied

        else:
            self.Q = self.Q.getCopy(negate=True)

    def __str__(self):
        if self.negateP:
            conj = " v ".join([str(l) for l in self.P])
        else:
            conj = " ∧ ".join([str(l) for l in self.P])
        return """{} v {}""".format(conj, self.Q)

class RemovedImplicClause(RemovedEquivClause):

    def __init__(self, P, Q):
        super().__init__(P,Q, True)

class ParameterClause:

    def __init__(self,lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    # Gets the clause as
    # a => b
    # instead of a <=> b
    def simplified(self):
        ret = []
        conj = "∧".join([str(l) for l in self.lhs])
        ret.append(conj + " => " + str(self.rhs))

        for l in self.lhs:
            ret.append(str(self.rhs) + " => " + str(l))

        return ret

    def removeEquiv(self):
        """removes P <=> Q in the parameter clauses and converts it to (~P v Q) & (P v ~Q)"""

        distributed_Or = []
        for v in self.lhs:
            distributed_Or.append(IndicatorClause([v.getCopy(), self.rhs.getCopy(negate=True)]))

        #return [RemovedEquivClause(self.lhs, neg_rhs_copy, False), RemovedEquivClause(self.lhs, rhs_copy, True)]
        return [RemovedEquivClause(self.lhs, self.rhs, True)] + distributed_Or

    def __str__(self):
        conj = " ∧ ".join([str(l) for l in self.lhs])
        return """{} <=> {}""".format(conj, self.rhs)


class ImplicationClause(ParameterClause):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def removeEquiv(self):
        """removes P => Q in the parameter clauses and converts it to ~P v Q"""
        return [RemovedImplicClause(self.lhs, self.rhs)]

    def __str__(self):
        conj = " ∧ ".join([str(l) for l in self.lhs])
        return """{} => {}""".format(conj, self.rhs)

class CNF:

    def __init__(self, bayes):
        self.vars = {}
        self.CPT = []
        self.bayes = bayes
        self.indicators = []
        self.paramClauses = []
        self.elimEquivClauses = []
        self.weights = []

    def elimEquiv(self):
        """
            https://en.wikipedia.org/wiki/Conjunctive_normal_form

            removes P <=> Q in the parameter clauses and converts it to (~P v Q) & (P v ~Q)
        """
        newParamClauses = []
        for clause in self.paramClauses:
            print("Converting: {}".format(clause))
            newParamClauses += clause.removeEquiv()
            print("into: {}".format("\n".join(str(p) for p in clause.removeEquiv())))

        self.elimEquivClauses = newParamClauses
        self.paramClauses = []
        return self

    def toDimac(self, toCachet=False):

        varToInt = {}
        i = 1

        for k, vars in self.vars.items():
            for v in vars:
                varToInt[str(v)] = i
                i += 1

        for c in self.CPT:
            varToInt[str(c)] = i
            i += 1

        if not toCachet:
            weights = ""
            # get weights

            for key, _ in sorted(varToInt.items(), key=lambda x: x[1]):
                for w in self.weights:
                    if str(w.lhs) == key:
                        weights += "{:.3f} ".format(float(w.prob))#str(w.prob) + " "

                for w in self.weights:
                    if str(w.lhs) == "~" + key:
                        #str(w.prob) + " "
                        weights += "{:.3f} ".format(float(w.prob))

            dimac = """\nc\nc Auto generated by script\nc\nc weights {}\np cnf {} {}\n""".format(
                weights, len(varToInt), len(self.indicators) + len(self.elimEquivClauses)
            )
        else:

            weights = []
            # get weights
            for key, _ in sorted(varToInt.items(), key=lambda x: x[1]):

                for w in self.weights:

                    if str(w.lhs) == key:
                        if type(w.lhs) == Variable:
                            weights.append(str(-1))
                        else:
                            weights.append(str(w.prob))

            dimac = """\nc\nc Auto generated by script for Cachet\nc\np cnf {} {}\n""".format(
                len(varToInt), len(self.indicators) + len(self.elimEquivClauses)
            )

            for i, w in enumerate(weights):
                dimac += "w {} {}\n".format((i + 1), w)

        #for k, v in varToInt.items():
        #    dimac += "c {} {}\n".format(k,v)

        for ind in self.indicators:
            for v in ind.vars:
                copy = v.getCopy()
                value = varToInt[copy.getBaseRepr()]
                if copy.negate:
                    value *= -1
                dimac += "{} ".format(value)

            dimac += "0\n"

        for p in self.paramClauses:
            rule_copy = []
            for v in p.lhs:
                copy = v.getCopy(negate=True)
                value = varToInt[copy.getBaseRepr()]
                if copy.negate:
                    value *= -1
                rule_copy.append(value)

            rule_copy.append(varToInt[str(p.rhs)])
            dimac += " ".join([str(v) for v in rule_copy])
            dimac += " 0\n"

        for clause in self.elimEquivClauses:
            if type(clause) is RemovedEquivClause or type(clause) is RemovedImplicClause:
                rule_copy = []
                for v in clause.P:
                    copy = v.getCopy()
                    value = varToInt[copy.getBaseRepr()]
                    if copy.negate:
                        value *= -1
                    rule_copy.append(value)

                val_Q = -varToInt[str(clause.Q.getCopy(negate=True))] if clause.Q.negate else varToInt[str(clause.Q)]
                rule_copy.append(val_Q)
                dimac += " ".join([str(v) for v in rule_copy])
                dimac += " 0\n"
            else:
                for v in clause.vars:
                    copy = v.getCopy()
                    value = varToInt[copy.getBaseRepr()]
                    if copy.negate:
                        value *= -1
                    dimac += "{} ".format(value)

                dimac += "0\n"

        return dimac
