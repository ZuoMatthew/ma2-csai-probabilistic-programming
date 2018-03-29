% Suppose we want to express two independent causes c1 and c2 that make an outcome e more likely. This is the typical case for a noisy-or gate:

0.5::c1. 0.5::c2.

0.3::e :- c1.
0.4::e :- c2.

evidence(c1,true).
evidence(c2,true).

query(e).