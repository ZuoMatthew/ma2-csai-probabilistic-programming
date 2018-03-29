0.1::inf(a).
0.1::inf(b).
0.1::initialInf(a).
0.1::initialInf(b).
0.1::contact(a,a).
0.1::contact(a,b).
0.1::contact(b,a).
0.1::contact(b,b).
0.6::inf(b) :- contact(b,a).
0.6::inf(b) :- contact(b,b).
0.6::inf(a) :- contact(a,a).
0.6::inf(a) :- contact(a,b).
inf(a) :- initialInf(a).
inf(b) :- initialInf(b).
query(inf(a)).
query(inf(b)).