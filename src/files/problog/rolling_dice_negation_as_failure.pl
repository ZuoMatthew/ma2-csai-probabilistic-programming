% Note that as in Prolog, negation has to be used with care, as it is only safe on ground goals. We illustrate this by posing non-ground queries (using an anonymous variable denoted by _ as argument) to the same program.

1/6::dice(1,D); 1/6::dice(2,D); 1/6::dice(3,D); 1/6::dice(4,D); 1/6::dice(5,D); 1/6::dice(6,D) :- die(D).

die(1).
die(2).

sum(S) :- dice(A,1), dice(B,2), S is A+B.
odd(D) :- dice(1,D).
odd(D) :- dice(3,D).
odd(D) :- dice(5,D).
even(D) :- \+ odd(D).

query(sum(_)).
evidence(even(1)).
evidence(odd(2)).