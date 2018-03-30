% converted from the bayesian network

0.01::burglary.
0.02::earthquake.
0.95::alarm :- burglary, earthquake.
0.94::alarm :- burglary, \+earthquake.
0.29::alarm :- \+burglary, earthquake.
0.001::alarm :- \+burglary, \+earthquake.
0.7::maryCalls :- alarm.
0.01::maryCalls :- \+alarm.
0.9::johnCalls :- alarm.
0.05::johnCalls :- \+alarm.

query(burglary).
query(earthquake).
query(alarm).
query(maryCalls).
query(johnCalls).