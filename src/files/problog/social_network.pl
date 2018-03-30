% The ProbLog program below encodes a variant of the famous Friends & Smokers problem. The first two rules state that there are two possible causes for a person X to smoke, namely X having stress, and X having a friend Y who smokes himself and influences X. Note that, according to our this program, the presence of stress and of (possibly multiple) smoking friends all contribute to the probability of the person X smoking, namely in a noisy-or way (recall the noisy-or in the coin tossing example). Furthermore, the program encodes that if X smokes, (s)he has asthma with probability 0.4.

0.3::stress(X) :- person(X).
0.2::influences(X,Y) :- person(X), person(Y).

smokes(X) :- stress(X).
smokes(X) :- friend(X,Y), influences(Y,X), smokes(Y).

0.4::asthma(X) :- smokes(X).

person(1).
person(2).
person(3).
person(4).

friend(1,2).
friend(2,1).
friend(2,4).
friend(3,2).
friend(4,2).

evidence(smokes(2),true).
evidence(influences(4,2),false).

% query(smokes(1)). % cannot do this one because of circular rules
query(smokes(3)).
query(smokes(4)).
% query(asthma(1)). % cannot do this one because of circular rules
query(asthma(2)).
query(asthma(3)).
query(asthma(4)).