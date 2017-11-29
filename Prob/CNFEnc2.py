from CNF import *
import copy
class CNFEnc2(CNF):

    def __init__(self, bayes):
        super(CNFEnc2, self).__init__(bayes)

    def _getVars(self):
        for node_name, node in self.bayes.getNodes().items():
            self.vars[node_name] = []
            for val in node.values:
                self.vars[node_name].append(Variable(node_name, val))

    def _getCPT_part(self, dependants, node, current_evidence):
        if len(dependants) == 0:
            for i,val in enumerate(node.values[:-1]):
                self.CPT.append(CPT(self.vars[node.name][i], val, current_evidence, "\\rho"))
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
        #
        # How to use this dict:
        # assume we have rho_B_b1|a1 and rho_B_b2|a1
        # index the dict as: dict[B][a1]
        # this would return a list of rho_B_b1|a1 and rho_B_b2|a1
        CPT_Dict = {}
        for cpt in self.CPT:
            if cpt.var.var not in CPT_Dict:
                CPT_Dict[cpt.var.var] = {}


            textVars = " ".join([v.var.value for v in cpt.conditional])
            if textVars not in CPT_Dict[cpt.var.var]:
                CPT_Dict[cpt.var.var][textVars] = []

            CPT_Dict[cpt.var.var][textVars].append(cpt)

        print(CPT_Dict)


        # {'A': {'[]': [ < CNF.CPT object at 0x109582b38 >]},
        # 'B': {"['a1']": [ < CNF.CPT object at 0x109588a90 >], "['a2']": [ < CNF.CPT object at 0x109588400 >]},
        # 'C': {"['a1']": [ < CNF.CPT object at 0x109588cc0 >, < CNF.CPT object at 0x109588128 >],
        #        "['a2']": [ < CNF.CPT object at 0x109588c50 >, < CNF.CPT object at 0x109588358 >]}}

        for key, vals in CPT_Dict.items():
            # key = 'C'
            # vals = {"['a1']": [ < CNF.CPT object at 0x109588cc0 >, < CNF.CPT object at 0x109588128 >],
            #        "['a2']": [ < CNF.CPT object at 0x109588c50 >, < CNF.CPT object at 0x109588358 >]}}
            for cond, cpt_rules in vals.items():
                # cond = ['a1']
                # cpt_rules = [ < CNF.CPT object at 0x109588cc0 >, < CNF.CPT object at 0x109588128 >]
                used_cpt = []

                for cpt in cpt_rules:
                    # negate previously used things
                    for c in used_cpt:
                        c.negate = True

                    used_cpt.append(copy.deepcopy(cpt))

                    conj = []
                    for c in cpt.conditional:
                        conj.append(c.var)

                    self.paramClauses.append(ParameterClause(conj + copy.deepcopy(used_cpt),cpt.var))


        #for key, vars in self.vars.items():
        #    converted_vars = [v.value for v in vars]

        #
        #     for i, v in enumerate(vars[:-1]):
        #         first_var = None
        #         conj = []
        #         for cpt in self.CPT:
        #             # We have the same base var
        #             if cpt.var.var == key:
        #                 if first_var is None:
        #                     first_var = [c.var for c in cpt.conditional]
        #
        #                     sameConditional = self._getCPTWithConditional([v.value for v in first_var],key,converted_vars,i)
        #                     print("conditionals: {} {} {} {}".format( [v.value for v in first_var],key,converted_vars,i))
        #                     for cond in sameConditional:
        #                         print("cond: {}".format(cond))
        #
        #
        #                 if converted_vars.index(cpt.var.value) < i:
        #
        #                     cpt_copy = copy.deepcopy(cpt)
        #                     cpt_copy.negative = True
        #                     conj.append(cpt_copy)
        #
        #                 elif converted_vars.index(cpt.var.value) == i:
        #                     conj.append(copy.deepcopy(cpt))
        #
        #         # conj = copy.deepcopy(cpt.conditional)
        #         # conj = [c.var for c in conj]
        #         # if cpt.value != v.value:
        #         #     cpt_copy = copy.deepcopy(cpt)
        #         #     cpt_copy.negative = True
        #         #     conj.append(cpt_copy)
        #         # else:
        #         #     conj.append(copy.deepcopy(cpt))
        #
        #         self.paramClauses.append(ParameterClause(conj + first_var,v))

    def convert(self):
        self._getVars()
        self._getCPT()
        self._getIndicatorClauses()

        # We got all the cpt
        # Now we have to create the rules
        self._getParamClauses()


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