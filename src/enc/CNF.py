import copy

def firstToUpper(strToUpper):
    return strToUpper[0].upper() + strToUpper[1:]

class Variable:

    def __init__(self, var, value, negate=False):
        self.var = var
        self.value = value
        self.negate = negate

    def getBaseRepr(self, isLatex=True):
        base = self.var + firstToUpper(self.value)
        if isLatex:
            return "$\lambda_{" + "{}".format(base) + "}$"
        else:
            return "\lambda_{" + "{}".format(base) + "}"

    def to_latex(self):
        base = self.getBaseRepr()
        if self.negate:
            return """$\\neg$ {}""".format(base)

        return base

    def __str__(self):
        base = self.getBaseRepr(False)
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

class Weight:

    def __init__(self, lhs, prob):
        self.lhs = lhs
        self.prob = prob

    def to_latex(self):
        return """W({}) = ${:.2f}$""".format(self.lhs.to_latex(), float(self.prob))

    def __str__(self):
        return """W({}) = {:.2f}""".format(self.lhs, float(self.prob))

class Conditional:

    def __init__(self, var):
        self.var = var

    def to_latex(self):
        base = self.var.var + firstToUpper(self.var.value)
        return """{}""".format(base)

    def __str__(self):
        base = self.var.var + firstToUpper(self.var.value)
        return """{}""".format(base)

    def asVar(self):
        return self.var


class CPT:

    def __init__(self, var, value, conditional, token="\\theta", negate=False):
        self.var = var
        self.value = value
        self.conditional = conditional
        self.token = token
        self.negate = negate

    def toggleNegate(self):
        self.negate = not self.negate


    def getBaseRepr(self, isLatex=True):
        if len(self.conditional) > 0:
            if isLatex:
                base = self.var.var + firstToUpper(self.var.value) + "|" + ",".join([c.to_latex() for c in self.conditional])
            else:
                base = self.var.var + firstToUpper(self.var.value) + "|" + ",".join([str(c) for c in self.conditional])

        else:
            base = self.var.var + firstToUpper(self.var.value)
        if isLatex:
            return """${}_""".format(self.token) + "{" + "{}".format(base) + "}$"
        else:
            return """{}_""".format(self.token) + "{" + "{}".format(base) + "}"

    def to_latex(self):
        base = self.getBaseRepr()
        if self.negate:
            return """$\\neg$ {}""".format(base)

        return base

    def __str__(self):
        base = self.getBaseRepr(False)
        if self.negate:
            return """~{}""".format(base)

        return base

    def getCopy(self, negate=False):
        c = copy.deepcopy(self)
        if negate:
            c.toggleNegate()
        return c

class IndicatorClause:

    def __init__(self, vars):
        self.vars = vars

    def to_latex(self):
        return " $\lor$ ".join([v.to_latex() for v in self.vars])

    def __str__(self):
        return " ∨ ".join([str(v) for v in self.vars])


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

    def to_latex(self):
        if self.negateP:
            conj = " $\lor$ ".join([l.to_latex() for l in self.P])
        else:
            conj = " $\land$ ".join([l.to_latex() for l in self.P])
        return """{} $\lor$ {}""".format(conj, self.Q)

    def __str__(self):
        if self.negateP:
            conj = " ∨ ".join([str(l) for l in self.P])
        else:
            conj = " ∧ ".join([str(l) for l in self.P])
        return """{} ∨ {}""".format(conj, self.Q)

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
        conj = "\land".join([str(l) for l in self.lhs])
        ret.append(conj + " \Rightarrow " + str(self.rhs))

        for l in self.lhs:
            ret.append(str(self.rhs) + " \Rightarrow " + str(l))

        return ret

    def removeEquiv(self):
        """removes P <=> Q in the parameter clauses and converts it to (~P v Q) & (P v ~Q)"""

        distributed_Or = []
        for v in self.lhs:
            distributed_Or.append(IndicatorClause([v.getCopy(), self.rhs.getCopy(negate=True)]))

        #return [RemovedEquivClause(self.lhs, neg_rhs_copy, False), RemovedEquivClause(self.lhs, rhs_copy, True)]
        return [RemovedEquivClause(self.lhs, self.rhs, True)] + distributed_Or

    def to_latex(self):
        conj = " \land ".join([l.to_latex() for l in self.lhs])
        return """{} \Leftrightarrow {}""".format(conj, self.rhs)

    def __str__(self):
        conj = " ∧ ".join([str(l) for l in self.lhs])
        return """{} ↔ {}""".format(conj, self.rhs)


class ImplicationClause(ParameterClause):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def removeEquiv(self):
        """removes P => Q in the parameter clauses and converts it to ~P v Q"""
        return [RemovedImplicClause(self.lhs, self.rhs)]

    def to_latex(self):
        conj = " \land ".join([l.to_latex() for l in self.lhs])
        return """{} \Rightarrow {}""".format(conj, self.rhs)

    def __str__(self):
        conj = " ∧ ".join([str(l) for l in self.lhs])
        return """{} ↔ {}""".format(conj, self.rhs)

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
                # First add the weight for var X
                for w in self.weights:
                    if str(w.lhs) == key:
                        weights += "{:.3f} ".format(float(w.prob))

                # then add its weight for var ~X (the negation of x)
                for w in self.weights:

                    if w.lhs.negate and key in str(w.lhs):
                    #if str(w.lhs) == "\\neg " + key:

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
                        if type(w.lhs) is Variable:
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
                value = varToInt[copy.getBaseRepr(False)]
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
                    value = varToInt[copy.getBaseRepr(False)]
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
                    value = varToInt[copy.getBaseRepr(False)]
                    if copy.negate:
                        value *= -1
                    dimac += "{} ".format(value)

                dimac += "0\n"

        return dimac
