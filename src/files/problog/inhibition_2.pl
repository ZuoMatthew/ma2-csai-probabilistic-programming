% In some cases, however, if both causes are present this reduces the likelihood of the effect happening. For example when the presence of a second drug blocks the impact of the original drug. In such a case we can use negated heads. Depending on the chosen probabilities the effect can be lower than the joint occurance of c1 and c2 or be lower then either p1 or p2:

0.5::c1. 0.5::c2.

0.3::e1 :- c1.
0.2::\+e1 :- c2.

0.4::e2 :- c2.
0.2::\+e2 :- c1.

e :- e1.
e :- e2.

evidence(c1,true).
evidence(c2,true).

query(e).