% An infectious disease spreads through a population as follows: when- ever two people are in regular contact with each other and one is infected, there is a probability of 0.6 of the infection spreading also to the other person. Given a set of initially infected people and a graph of connections between individuals in the population, the goal is to predict the spread of the disease.

person(a).
person(b).

0.1::initialInf(X) :- person(X).
0.1::inf(X) :- person(X).
0.1::contact(X,Y) :- person(X), person(Y).

inf(X)      :- initialInf(X).
0.6::inf(X) :- contact(X, Y), inf(Y).

query(inf(_)).