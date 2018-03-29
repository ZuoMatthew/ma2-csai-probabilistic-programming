% Note that this program uses several Prolog builtins such as support for lists and arithmetic. The program also uses another feature of ProbLog2, namely support for (intensional) probabilistic facts with a `flexible’ probability. This means that the probability is not prespecified but is an arithmetic expression that needs to be computed. In the program, this is used in the intensional probabilistic fact “P::pack(Item) :- …”, which says that the probability of packing an item is inversely proportional to its weight. Such a flexible probability can be used in ProbLog2 under the restriction that the arithmetic expression can be evaluated at call-time (i.e., by the time the probabilistic fact is reached by SLD resolution to prove the queries and evidence).

weight(skis,6).
weight(boots,4).
weight(helmet,3).
weight(gloves,2).

% intensional probabilistic fact with flexible probability:
P::pack(Item) :- weight(Item,Weight),  P is 1.0/Weight.

excess(Limit) :- excess([skis,boots,helmet,gloves],Limit). % all possible items
excess([],Limit) :- Limit<0.
excess([I|R],Limit) :- pack(I), weight(I,W), L is Limit-W, excess(R,L).
excess([I|R],Limit) :- \+pack(I), excess(R,Limit).
query(excess(8)).