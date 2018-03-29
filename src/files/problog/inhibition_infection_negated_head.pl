% A solution in which we can keep our original “default” rule unchanged is not possible using noisy-or or is not intuitive to impossible in current probabilistic logics. Indeed, this is an obvious consequence of the fact that adding additional rules can only increase probabilities. In this paper, we introduce the new feature of negation in the head of rules, which will allow us to represent also a decrease in probabilities. In particular, we will be able to represent our example as:

person(a).
person(b).

0.1::initialInf(X) :- person(X).
0.1::inf(X) :- person(X).
0.1::contact(X,Y) :- person(X), person(Y).
0.1::riskyTravel(X) :- person(X).
0.1::resistant(X) :- person(X).

inf(X)         :- initialInf(X).
0.6::inf(X)    :- contact(X, Y), inf(Y).
0.33::\+inf(X) :- resistant(X).
0.2::inf(X)    :- riskyTravel(X).

query(inf(_)).