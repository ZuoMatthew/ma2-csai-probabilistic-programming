0.7::burglary.
0.2::earthquake.

0.9::alarm :- burglary, earthquake.
0.8::alarm :- burglary, \+earthquake.
0.1::alarm :- \+burglary, earthquake.

evidence(alarm,true).
query(alarm).
query(burglary).
query(earthquake).

0.8::a ; 0.7::b :- c.
a :- c, p_a_0.
b :- c, p_b_0.



