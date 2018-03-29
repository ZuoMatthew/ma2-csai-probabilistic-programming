% Let’s consider an infinite number of dice, which we roll one after the other until we see a six for the first time. What is the probability of stopping after n dice? The first die is always rolled, those with higher numbers D are only rolled if the previous roll did not stop the process. We use the builtin predicate between/3 to restrict querying to n = 1,2,3,4,5.

1/6::dice(1,1); 1/6::dice(2,1); 1/6::dice(3,1); 1/6::dice(4,1); 1/6::dice(5,1); 1/6::dice(6,1).
1/6::dice(1,D); 1/6::dice(2,D); 1/6::dice(3,D); 1/6::dice(4,D); 1/6::dice(5,D); 1/6::dice(6,D) :- D > 1, P is D-1, continue(P).

stop(N) :- dice(6,N).
continue(N) :- dice(X,N), X < 6.

query(stop(N)) :- between(1,5,N).

% closed form probability computation
%query(s(X)) :- between(1,5,X).
%P::s(N) :- P is 1/6*(5/6)**(N-1).