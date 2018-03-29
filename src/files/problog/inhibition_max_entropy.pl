% A maximum-entropy choice of value for cancellation parameters, designed specifically for describing partial cancellation, equals 1/2. The results are:

0.5::c1. % prior
0.5::c2. % prior

0.8::xc1 :- c1. % p_1
0.5::\+xc1 :- c1, c2. % \alpha_{1|12}

0.3::xc2 :- c2. % p_2
0.5::\+xc2 :- c1, c2. % \alpha_{2|12}

e :- xc1.
e :- xc2.

evidence(c1,true).
evidence(c2,true).
query(e).