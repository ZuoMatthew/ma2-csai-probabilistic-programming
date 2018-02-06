from CNF import *
import copy
class CNFEnc1(CNF):


    def __init__(self, bayes):
        super(CNFEnc1, self).__init__(bayes)

    def _getVars(self):
        for node_name, node in self.bayes.getNodes().items():
            self.vars[node_name] = []
            for val in node.values:
                self.vars[node_name].append(Variable(node_name, val))

    def _getCPT_part(self, dependants, node, current_evidence):
        if len(dependants) == 0:
            for i,val in enumerate(node.values):
                self.CPT.append(CPT(self.vars[node.name][i], val, current_evidence))
        else:
            for i,v in enumerate(dependants[0].values):
                cond = Conditional(copy.deepcopy(self.vars[dependants[0].name][i]))
                evid = copy.deepcopy(current_evidence)
                evid.append(cond)
                self._getCPT_part(dependants[1:], node, evid)


    def _getCPT(self):
        for node_name, node in self.bayes.getNodes().items():
            dependants = node.probabilities.dependents
            self._getCPT_part(dependants, node, [])


    def _getIndicatorClauses(self):
        for name, vars in self.vars.items():
            num_vars = len(vars)
            for i in range(0, num_vars):

                for j in range(i+1, num_vars):
                    var1 = copy.deepcopy(vars[i])
                    var2 = copy.deepcopy(vars[j])
                    var1.negate = True
                    var2.negate = True
                    self.indicators.append(IndicatorClause([var1, var2]))

            self.indicators.append(IndicatorClause(vars))

    def _getParamClauses(self):
        for cpt in self.CPT:
            lhs = copy.deepcopy(cpt.conditional)
            lhs = [l.asVar() for l in lhs]
            lhs.append(copy.deepcopy(cpt.var))
            self.paramClauses.append(ParameterClause(lhs, cpt))

    def _assignWeights(self):
        for k, values in self.vars.items():
            for v in values:
                self.weights.append(Weight(copy.deepcopy(v), 1))
                neg = copy.deepcopy(v)
                neg.negate = True
                self.weights.append(Weight(neg, 1))

        for cpt in self.CPT:
            probFunc = self.bayes.getProbabilityFunction(cpt.var.var)
            d = {"value": cpt.value}
            for j in cpt.conditional:
                d[j.var.var] = j.var.value
            self.weights.append(Weight(copy.deepcopy(cpt), probFunc.get(d)))
            self.weights.append(Weight(cpt.getCopy(negate=True), probFunc.get(d)))


    def convert(self):
        self._getVars()
        self._getCPT()
        self._getIndicatorClauses()
        self._getParamClauses()
        self._assignWeights()

    def __str__(self):
        enc = "Indicator clauses: \n"
        for i in self.indicators:
            enc += str(i) + "\n"

        enc += "Parameter clauses: \n"
        for p in self.paramClauses:
            enc += str(p) + "\n"

        enc += "Weights: \n"
        for w in self.weights:
            enc += str(w) + "\n"


        return enc